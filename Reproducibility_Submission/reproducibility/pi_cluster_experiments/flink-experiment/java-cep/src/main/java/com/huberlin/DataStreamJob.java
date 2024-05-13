/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.huberlin;

import java.io.*;
import java.lang.*;
import static java.lang.Thread.sleep;
import java.net.*;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.*;
import java.util.*;
import java.util.concurrent.*;

import org.apache.flink.configuration.Configuration;
import org.apache.flink.configuration.GlobalConfiguration;

import org.apache.flink.core.fs.FileSystem;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.KeyedStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.functions.source.RichSourceFunction;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;


import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;

import org.apache.flink.cep.*;
import org.apache.flink.streaming.api.*;
import org.apache.flink.streaming.api.watermark.*;
import org.apache.flink.streaming.api.windowing.time.*;

import org.apache.flink.api.common.functions.*;
import org.apache.flink.api.java.functions.KeySelector;

import org.apache.flink.streaming.api.TimeCharacteristic;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.functions.timestamps.BoundedOutOfOrdernessTimestampExtractor;
import org.apache.flink.streaming.api.functions.AssignerWithPeriodicWatermarks;

import org.json.JSONException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

 
public class DataStreamJob
{	
    
    private static List<String> connections_to_establish = new ArrayList<String>();
    
    private static Map<String, String> nodeID_to_forwarding_ip = new HashMap<String, String>();
    
    private static List<String> event_types_to_forward = new ArrayList<String>();
    
    private static List<String> event_types_to_process = new ArrayList<String>();
    
    private static Map<String, Long> ip_to_newest_watermarking_timestamp = Collections.synchronizedMap(new HashMap<>());

    private static String own_ID = "";
    
    private static long current_global_watermark = 0;

    
    public static class JSONConfigLoader
    {
    	
        public static String ID = "";
    	public static String path = "";
    	public JSONConfigLoader(String path, String ID) {
    	        this.path = path;
    	        this.ID = ID;
    	    }
        public static void LoadJSONConfig()
        {            
            try {
                JSONParser parser = new JSONParser();
                
                JSONObject json_object = (JSONObject) parser.parse(new FileReader(path));
                JSONObject json_topology_config = (JSONObject)json_object.get(ID);
                System.out.println("own_ID:"+ID);
                JSONObject forwarding_table = (JSONObject)json_topology_config.get("forwarding_table");

                for (Object nodeID : forwarding_table.keySet())
                {
                    String nodeID_str = (String) nodeID;
                    System.out.println(nodeID_str);
                    
                    String forwarding_node_ip = (String) forwarding_table.get(nodeID_str);
                                                
                    //lambda for creating a new arraylist, if key was abscent; else add the ip to the list
                    nodeID_to_forwarding_ip.put(nodeID_str, forwarding_node_ip);
                    System.out.println(forwarding_node_ip);
                }
                
                JSONArray connections = (JSONArray)json_topology_config.get("connection");
                for (int i = 0; i < connections.size(); i++) 
                {
                    String connection = (String) connections.get(i);
                    connections_to_establish.add(connection);
                    System.out.println(connection);
                }
                
                own_ID = (String) json_topology_config.get("own_ID");
                System.out.println("own_ID:"+own_ID);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            catch (IOException e) {
                e.printStackTrace();
            }
            catch (JSONException e) {
                e.printStackTrace();
            }  
            catch (ParseException e) {
                e.printStackTrace();
            }

        }

    }
    
    
	public static class Event
	{        
        private String eventType;
        private String timestamp_hhmmssms;
		private long timestamp;
        private String ID;
        private Instant creationDateAndTimeInstant;
        private long bikeID;
        private String target_nodeID;
        private String source_node_ip;
		
		public Event() {}
		
		public Event(String eventType, String timestamp_hhmmssms, String eventID, String creationTime, String bike_id, String target_nodeID, String source_node_ip)
		{
			this.eventType = eventType;
            this.timestamp_hhmmssms = timestamp_hhmmssms;
            this.ID = eventID;
            String[] hoursMinutesSecondsMilliseconds = timestamp_hhmmssms.split(":");
			long resulting_timestamp = 0;
            if (hoursMinutesSecondsMilliseconds.length == 3)
            {
                resulting_timestamp += Long.parseLong(hoursMinutesSecondsMilliseconds[0], 10) * 60 * 60 * 1000;
                resulting_timestamp += Long.parseLong(hoursMinutesSecondsMilliseconds[1], 10) * 60 * 1000;
                resulting_timestamp += Long.parseLong(hoursMinutesSecondsMilliseconds[2], 10) * 1000;
                this.timestamp = resulting_timestamp;	
            }else if (hoursMinutesSecondsMilliseconds.length == 4)
            {
                resulting_timestamp += Long.parseLong(hoursMinutesSecondsMilliseconds[0], 10) * 60 * 60 * 1000;
                resulting_timestamp += Long.parseLong(hoursMinutesSecondsMilliseconds[1], 10) * 60 * 1000;
                resulting_timestamp += Long.parseLong(hoursMinutesSecondsMilliseconds[2], 10) * 1000;
                resulting_timestamp += Long.parseLong(hoursMinutesSecondsMilliseconds[3], 10);
                this.timestamp = resulting_timestamp;	
            }
            
            //remove T and Z from date format to avoid errorneous parsing afterwards
            if (creationTime.contains("Z"))
            {
                creationTime = creationTime.replace("T", " ");
                creationTime = creationTime.replace("Z", "");
            }
            
            //System.out.println("creationTime: " + creationTime);
            this.creationDateAndTimeInstant = Timestamp.valueOf(creationTime).toInstant();

            this.bikeID = Long.parseLong(bike_id, 10);
            
            this.target_nodeID = target_nodeID;
            this.source_node_ip = source_node_ip;
		}
		
		public static Event parse(String received)
		{
			String[] receivedParts = received.split("\\|");

            return new Event(receivedParts[0].trim(), receivedParts[1].trim(), receivedParts[2].trim(), receivedParts[3].trim(), receivedParts[4].trim(), receivedParts[5].trim(), receivedParts[6].trim());
		}

		public String getEventtype()
		{
			return eventType;
		}
		
		public long getTimestamp()
		{            
			return timestamp;
		}
        
        public long getBikeID()
        {
            return bikeID;
        }
        
        public String getTargetNodeID()
        {
            return target_nodeID;
        }

        public String getSourceNodeIp()
        {
            return source_node_ip;
        }
		
		// Implemented toString() so generic print() can be called on Event-type 
		public String toString()
		{
            String eventString = eventType;
            eventString+= " | " + timestamp_hhmmssms;
            eventString+= " | " + ID;
            eventString+= " | " + creationDateAndTimeInstant;
            //eventString+= " | " + timestamp;
            eventString+= " | " + bikeID;
            eventString+= " | " + target_nodeID;
            eventString+= " | " + source_node_ip;
            return eventString;
		}
	}

	private static class EventWithSource
	{
		public Event event;
		public String ip;

		public EventWithSource(Event event, String ip)
		{
			this.event = event;
			this.ip = ip;
		}

		public String toString()
		{
			return ip + ": " + event;
		}
	};

	public static IterativeCondition<Event> sequence_condition_bikeid(String type, String previous)
	{
		return new IterativeCondition<Event>() 
        {
			@Override
			public boolean filter(Event evt, Context<Event> ctx) throws Exception 
			{
				if (evt.getEventtype().equals(type)) 
				{
                    
					for (Event event : ctx.getEventsForPattern(previous))
					{   
                        if (event.getBikeID() != evt.getBikeID())
                            return false;
					}
					return true;
				}
				return false;
			}
		};
	}
  
    static Instant lastUpdateTime = Instant.now();
    static long countEventsProcessed = 0;

    public static void measureThroughput()
    {
        long previousCountEventsProcessed = 0;
        long secondsPassed = 0;
        while(true)
        {
            try 
            {
                Thread.sleep(1000);            
            } catch(InterruptedException ex) 
            {
                Thread.currentThread().interrupt();
            }
            System.out.println(++secondsPassed + "seconds have passed; Throughput per second:" + (countEventsProcessed - previousCountEventsProcessed));
            previousCountEventsProcessed = countEventsProcessed;
        }
    }

  
	public static void main(String[] args) throws Exception
	{
		Configuration conf = new Configuration();
		StreamExecutionEnvironment env = StreamExecutionEnvironment.createLocalEnvironmentWithWebUI(conf);
		env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        final Configuration flinkConfig = GlobalConfiguration.loadConfiguration("conf");
        FileSystem.initialize(flinkConfig);
        if (args.length == 0) {
        	int query = 1;
        	String path = "";
        }
        int query = Integer.parseInt(args[0]);
        String path = args[1];
        String ID = args[2];
        System.out.println("my ID" + ID);
        
        new Thread(() -> { measureThroughput(); }).start();
        
        // Only one engine-thread will work (output is displayed in the same way the packets arrive)
		env.setParallelism(1);

        //load the json file which contains information about the network topology and connections to be established
        JSONConfigLoader json_config = new JSONConfigLoader(path, ID);
        json_config.LoadJSONConfig();
        
        System.out.println("It starts..");
        for (String ip : connections_to_establish)
            System.out.println(ip);
        
        System.out.println("What happended until now?");
        for (String key : nodeID_to_forwarding_ip.keySet()) 
        {
            System.out.println(key);
            System.out.println(nodeID_to_forwarding_ip.get(key));
        }
        
        System.out.println("Events to forward:");
        for (String e : event_types_to_forward)
            System.out.println(e);
        
        System.out.println("Events to process:");
        for (String e : event_types_to_process)
            System.out.println(e);

		DataStream<EventWithSource> inputStream = env.addSource(new RichSourceFunction<EventWithSource>()
		{
			private volatile boolean isCancelled;
			private Thread accepting_thread;
			private BlockingQueue<EventWithSource> merged_event_stream;


			public void handleClient(Socket socket)
			{
				try
				{
					BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
					String client_address = socket.getRemoteSocketAddress().toString();
					while(!isCancelled)
					{
						String message = input.readLine();
                        
                        if (message == null)
                            continue;
                            
                        //check, if a client has sent his entire event stream..
                        if (message.contains("end-of-the-stream"))
                        {
                            //set the watermark to the highest possible value to be not considered anymore
                            ip_to_newest_watermarking_timestamp.put(client_address, Long.MAX_VALUE);
                            System.out.println("Reached the end of the stream for "+client_address+"->"+ip_to_newest_watermarking_timestamp.get(client_address));
                        }
                        //.. else, simply process the incoming event accordingly
                        else
                        {
                            if (!message.contains("|"))
                                continue;
                                
                            Event event = Event.parse(message);
                            //System.out.println("New event " + event + " from:" + event.getSourceNodeIp());
                            if (!ip_to_newest_watermarking_timestamp.containsKey(event.getSourceNodeIp()))
                                System.out.println("New source node ip: " + event.getSourceNodeIp());
                            //update watermark for a sending node
                            ip_to_newest_watermarking_timestamp.put(event.getSourceNodeIp(), event.getTimestamp());

                            merged_event_stream.put(new EventWithSource(event,event.getSourceNodeIp()));

                        }

					}
				}
				catch(IOException e)
				{
					System.err.print("Client disconnected");
				}
				catch(InterruptedException e)
				{
					System.err.print("Client disconnected");
				}
			}

            public void updateWatermark(EventWithSource event, SourceContext<EventWithSource> sourceContext)
            {
                long oldestTimestamp = Long.MAX_VALUE;
                String client_address = "";

                //if not every node has sent an event yet, wait for it to update the watermark
                if (connections_to_establish.size() > ip_to_newest_watermarking_timestamp.size())
                {
                    System.out.println("Not everyone has connected yet!" + connections_to_establish.size() + " vs. " + ip_to_newest_watermarking_timestamp.size());
                    return;
                 }
                
                for (String client_address_watermark_key : ip_to_newest_watermarking_timestamp.keySet())
                {
                    if (ip_to_newest_watermarking_timestamp.get(client_address_watermark_key) < oldestTimestamp)
                    {
                        oldestTimestamp = ip_to_newest_watermarking_timestamp.get(client_address_watermark_key);
                        client_address = client_address_watermark_key;
                    }
                }


                if (oldestTimestamp < Long.MAX_VALUE && current_global_watermark < (oldestTimestamp-1))
                {                  
                    //update watermark
                    current_global_watermark = oldestTimestamp-1;
                    sourceContext.emitWatermark(new Watermark(oldestTimestamp-1)); 
                }
            }


			@Override
			public void run(SourceContext<EventWithSource> sourceContext) throws Exception
			{
				while (!isCancelled)
				{
                    //retrieve and remove the head of the queue (event stream)
					EventWithSource event = merged_event_stream.take();

                    //process it with Flink
					sourceContext.collectWithTimestamp(event, event.event.getTimestamp());
                    
                    updateWatermark(event, sourceContext);

	        	}
	         }

	         @Override
	         public void cancel()
			 {
	        	 isCancelled = true;
	         }
	
	         @Override
	         public void open(Configuration parameters) throws Exception
			 {
				super.open(parameters);

				merged_event_stream = new LinkedBlockingQueue<EventWithSource>();

				accepting_thread = new Thread(new Runnable()
				{
					public void run()
					{
						try
						{
							ServerSocket socket = new ServerSocket(5005);
							while(!isCancelled)
							{
								Socket new_client = socket.accept();
								new Thread(() -> { handleClient(new_client); }).start();
								System.out.println("New client " + new_client.getRemoteSocketAddress().toString() + " connected");
							}
						}
						catch(IOException e)
						{
							System.err.print("Unacceptable");
						}
					}
				});
				accepting_thread.start();
	         }

	    });


		DataStream<Event> locallyProcessedEventStream = inputStream.filter(new FilterFunction<EventWithSource>()
		{
			@Override
			public boolean filter(EventWithSource e) throws Exception
			{
                //if a node is the target node, process the event locally
				return own_ID.equals(e.event.target_nodeID);
			}
		}).map(new MapFunction<EventWithSource,Event>()
		{
			@Override
			public Event map(EventWithSource event) throws Exception
			{
                ++countEventsProcessed;
				return event.event;
			}
		});
        //locallyProcessedEventStream.print();

        //maybe add a .map to return the event without an ip (as the source is probably not required for the forwarding)
		DataStream<EventWithSource> toForwardEventStream = inputStream.filter(new FilterFunction<EventWithSource>()
		{
			@Override
			public boolean filter(EventWithSource e) throws Exception
			{
				return !own_ID.equals(e.event.target_nodeID);
			}
		});
        //toForwardEventStream.print();

        //Query Q1 AND(E,F,G,H)
        IterativeCondition<Event> q1_conjunction_condition = new IterativeCondition<Event>() 
        {
			@Override
			public boolean filter(Event evt, Context<Event> ctx) throws Exception 
			{
				if (evt.getEventtype().equals("E") || evt.getEventtype().equals("F") || evt.getEventtype().equals("G") || evt.getEventtype().equals("H")) 
				{
					for (Event event : ctx.getEventsForPattern("first"))
					{
						if (event.getEventtype().equals(evt.getEventtype()))
							return false;
                        
                        
                        if (evt.getEventtype().equals("H") || event.getEventtype().equals("H"))
                            continue;
                            
                        if (event.getBikeID() != evt.getBikeID())
                            return false;

					}
					return true;
				}
				return false;
			}
		};
        
        Pattern<Event, ?> query1Pattern = Pattern.<Event> begin("first").where(q1_conjunction_condition).times(4).allowCombinations().within(Time.seconds(86400));


        //Query Q2 SEQ(C,D,E,I)
		Pattern<Event, ?> query2Pattern = Pattern.<Event> begin("first").where(sequence_condition_bikeid("C",""))
			.followedByAny("second").where(sequence_condition_bikeid("D","first"))
            .followedByAny("third").where(sequence_condition_bikeid("E","second"))
            .followedByAny("fourth").where(sequence_condition_bikeid("I","third"))
            .within(Time.seconds(86400));

        
        
        //Query Q3 AND(A,SEQ(D,I),F) 
        IterativeCondition<Event> q3_conjunction_condition = new IterativeCondition<Event>() 
        {
			@Override
			public boolean filter(Event evt, Context<Event> ctx) throws Exception 
			{
				if (evt.getEventtype().equals("A") || evt.getEventtype().equals("D") || evt.getEventtype().equals("I") || evt.getEventtype().equals("F")) 
				{
					Long d_time = null, i_time = null;

					for (Event event : ctx.getEventsForPattern("first"))
					{
						if (event.getEventtype().equals(evt.getEventtype()))
							return false;
                            
                        if (event.getBikeID() != evt.getBikeID())
                            return false;
						
						if(event.getEventtype().equals("D")) d_time = event.getTimestamp();
						if(event.getEventtype().equals("I")) i_time = event.getTimestamp();
					}

					if(evt.getEventtype().equals("D")) d_time = evt.getTimestamp();
					if(evt.getEventtype().equals("I")) i_time = evt.getTimestamp();

					if(d_time!=null && i_time!=null)
					{
						if(d_time>i_time) return false;
						for (Event event : ctx.getEventsForPattern("first"))
						{
							if(event.getEventtype().equals("D") || event.getEventtype().equals("I")) continue;
							if(event.getTimestamp()>d_time && event.getTimestamp()<i_time) return false;
						}
					}

					return true;
				}
				return false;
			}
		};
        
        Pattern<Event, ?> query3Pattern = Pattern.<Event> begin("first").where(q3_conjunction_condition).times(4).allowCombinations().within(Time.seconds(86400));
        
        
        //QWL Q4 & Q5
        //Q4 SEQ(A,AND(B,I),E)
        IterativeCondition<Event> q4_conjunction_condition = new IterativeCondition<Event>() 
        {
			@Override
			public boolean filter(Event evt, Context<Event> ctx) throws Exception 
			{
				Long a_time = null, bi_time = null, e_time = null;

				if (evt.getEventtype().equals("A") || evt.getEventtype().equals("B") || evt.getEventtype().equals("I") || evt.getEventtype().equals("E")) 
				{

                    for (Event event : ctx.getEventsForPattern("first"))
                    {
                        if (event.getEventtype().equals(evt.getEventtype()))
                            return false;

                        if (event.getEventtype().equals("B") && evt.getEventtype().equals("I"))
                            return false;
                        if (event.getEventtype().equals("I") && evt.getEventtype().equals("B"))
                            return false;
                            
                        if (event.getBikeID() != evt.getBikeID())
                            return false;
                        
                        if(event.getEventtype().equals("A")) a_time = event.getTimestamp();
                        if(event.getEventtype().equals("B") || event.getEventtype().equals("I")) bi_time = event.getTimestamp();
                        if(event.getEventtype().equals("E")) e_time = event.getTimestamp();
                    }

                    if(evt.getEventtype().equals("A")) a_time = evt.getTimestamp();
                    if(evt.getEventtype().equals("B") || evt.getEventtype().equals("I")) bi_time = evt.getTimestamp();
                    if(evt.getEventtype().equals("E")) e_time = evt.getTimestamp();
        
                    if(a_time!=null)
                    {
                        for(Long time: new Long[]{bi_time,e_time})
                            if(time!=null && time<a_time)
                                return false;
                    }
                    
                    if(e_time!=null)
                    {
                        for(Long time: new Long[]{bi_time,a_time})
                            if(time!=null && time>e_time)
                                return false;
                    }
                    return true;
                }
				return false;
			}
		};
        
        Pattern<Event, ?> query4Pattern = Pattern.<Event> begin("first").where(q4_conjunction_condition).times(4).allowCombinations().within(Time.seconds(86400));
        
        
        //Q5 AND(E,F,C,H)
        IterativeCondition<Event> q5_conjunction_condition = new IterativeCondition<Event>() 
        {
			@Override
			public boolean filter(Event evt, Context<Event> ctx) throws Exception 
			{
				if (evt.getEventtype().equals("E") || evt.getEventtype().equals("F") || evt.getEventtype().equals("C") || evt.getEventtype().equals("H")) 
				{
					for (Event event : ctx.getEventsForPattern("first"))
					{
						if (event.getEventtype().equals(evt.getEventtype()))
							return false;
                        
                        if (evt.getEventtype().equals("C") || event.getEventtype().equals("C"))
                            continue;
                        
                        if (event.getBikeID() != evt.getBikeID())
                            return false;
					}
					return true;
				}
				return false;
			}
		};
        
        Pattern<Event, ?> query5Pattern = Pattern.<Event> begin("first").where(q5_conjunction_condition).times(4).allowCombinations().within(Time.seconds(86400));

        Pattern<Event, ?> pattern = null;
        Pattern<Event, ?> pattern2 = null;

        if (query == 1) {
            pattern = query1Pattern;
        } else if (query == 2) {
            pattern = query2Pattern;
        } else if (query == 3) {
            pattern = query3Pattern;
        }
        else if (query == 4) {
        	pattern = query4Pattern;
        	pattern2 = query5Pattern;
        }
        
        
        // apply pattern to Datastream
        PatternStream<Event> matchANDStream = CEP.pattern(locallyProcessedEventStream, pattern); 
	    
	    DataStream<String> outputANDStream = matchANDStream.select(new PatternSelectFunction<Event, String>() 
        {
                public Instant adjust_instant_timestamp(Instant timestamp_to_convert)
                {
                    String tmp = timestamp_to_convert.toString();

                    int idx = tmp.indexOf("T");
                    String substring_to_replace = tmp.substring(idx,idx+3);

                    tmp = tmp.replaceAll(substring_to_replace,"T02");
                    tmp = tmp.replace("T", " ");
                    tmp = tmp.replace("Z", "");

                    return Timestamp.valueOf(tmp).toInstant();
                    
                }
            
		      @Override
		      public String select(Map<String, List<Event>> match) throws Exception 
              {
                  Instant complexEventCreationTime = Instant.now();
                  Instant latestDateAndTimeInstant = java.sql.Timestamp.valueOf("2000-01-01 01:01:010.0").toInstant();
                  String complexEvent = "";
                  boolean first_run = true;
                  
                  
                  if (match.get("first").size() == 1)
                  {
                      for (Event evt : new Event[]{match.get("first").get(0),match.get("second").get(0),match.get("third").get(0),match.get("fourth").get(0)})
                      {
                          if (first_run)
                          {
                              latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              first_run = false;
                          }
                          else
                          {
                              if (latestDateAndTimeInstant.isBefore(evt.creationDateAndTimeInstant))
                              {
                                  latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              }
                          }
                          complexEvent += ("(" + evt.getEventtype() + " - " + evt.bikeID + " - " + evt.creationDateAndTimeInstant + ") - ");
                      }
                      
                      complexEvent += "detection latency:"+Duration.between(adjust_instant_timestamp(latestDateAndTimeInstant), adjust_instant_timestamp(complexEventCreationTime)).toMillis();
                  }
                  else
                  {
                      for (Event evt : match.get("first"))
                      {
                          if (first_run)
                          {
                              latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              first_run = false;
                          }
                          else
                          {
                              if (latestDateAndTimeInstant.isBefore(evt.creationDateAndTimeInstant))
                              {
                                  latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              }
                          }
                          complexEvent += ("(" + evt.getEventtype() + " - " + evt.bikeID + " - " + evt.creationDateAndTimeInstant + ") - ");
                      }

                    complexEvent += "detection latency:"+Duration.between(adjust_instant_timestamp(latestDateAndTimeInstant), adjust_instant_timestamp(complexEventCreationTime)).toMillis();
                  }
                  
                  return complexEvent;
		      }
              
	    });
	    
		//add Sink method decides what to do with the resulting event stream
	    outputANDStream.addSink(new RichSinkFunction<String>()
		{    
	    	@Override
	        public void invoke(String evt, Context context) throws Exception
			{
	            System.out.println(evt);
	    	}
	    });
        
        if (query == 4){
        // apply pattern to Datastream
        PatternStream<Event> matchANDStream2 = CEP.pattern(locallyProcessedEventStream, pattern2);
	    
	    DataStream<String> outputANDStream2 = matchANDStream2.select(new PatternSelectFunction<Event, String>() 
        {
            
                public Instant adjust_instant_timestamp(Instant timestamp_to_convert)
                {
                    String tmp = timestamp_to_convert.toString();

                    int idx = tmp.indexOf("T");
                    String substring_to_replace = tmp.substring(idx,idx+3);

                    tmp = tmp.replaceAll(substring_to_replace,"T02");
                    tmp = tmp.replace("T", " ");
                    tmp = tmp.replace("Z", "");

                    return Timestamp.valueOf(tmp).toInstant();
                    
                }
            
            
		      @Override
		      public String select(Map<String, List<Event>> match) throws Exception 
              {
                  Instant complexEventCreationTime = Instant.now();
                  Instant latestDateAndTimeInstant = java.sql.Timestamp.valueOf("2000-01-01 01:01:010.0").toInstant();
                  String complexEvent = "";
                  boolean first_run = true;
                  
                  
                  if (match.get("first").size() == 1)
                  {
                      for (Event evt : new Event[]{match.get("first").get(0),match.get("second").get(0),match.get("thrid").get(0),match.get("fourth").get(0)})//,match.get("third")[0]})
                      {
                          if (first_run)
                          {
                              latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              first_run = false;
                          }
                          else
                          {
                              if (latestDateAndTimeInstant.isBefore(evt.creationDateAndTimeInstant))
                              {
                                  latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              }
                          }
                          complexEvent += ("(" + evt.getEventtype() + " - " + evt.bikeID + " - " + evt.creationDateAndTimeInstant + ") - ");
                      }
                      
                      complexEvent += "detection latency:"+Duration.between(adjust_instant_timestamp(latestDateAndTimeInstant), adjust_instant_timestamp(complexEventCreationTime)).toMillis();
                  }
                  else
                  {
                      for (Event evt : match.get("first"))
                      {
                          if (first_run)
                          {
                              latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              first_run = false;
                          }
                          else
                          {
                              if (latestDateAndTimeInstant.isBefore(evt.creationDateAndTimeInstant))
                              {
                                  latestDateAndTimeInstant = evt.creationDateAndTimeInstant;
                              }
                          }
                          complexEvent += ("(" + evt.getEventtype() + " - " + evt.bikeID + " - " + evt.creationDateAndTimeInstant + ") - ");
                      }

                      complexEvent += "detection latency:"+Duration.between(adjust_instant_timestamp(latestDateAndTimeInstant), adjust_instant_timestamp(complexEventCreationTime)).toMillis();
                  }
                  
                  return complexEvent;
		      }
              
	    });
	    
		//add Sink method decides what to do with the resulting event stream
	    outputANDStream2.addSink(new RichSinkFunction<String>()
		{    
	    	@Override
	        public void invoke(String evt, Context context) throws Exception
			{
	            System.out.println(evt);
	    	}
	    });
        }
        
        
		toForwardEventStream.addSink(new RichSinkFunction<EventWithSource>()
		{    
	    	@Override
	        public void invoke(EventWithSource event, Context context) throws Exception
			{
                
				String target_ip = nodeID_to_forwarding_ip.get(event.event.getTargetNodeID());
                //System.out.println("event.event.getTargetNodeID(): " + event.event.getTargetNodeID() + " -> target ip: " + target_ip);
                forward(event.event, target_ip);
	    	}
            
            
			private void forward(Event event, String target_ip)
			{
				try
				{
                    //if the connection to a forwarding target was not established yet then establish it
					if(!connections.containsKey(target_ip))
					{
                        String[] ip = target_ip.split(":");
                        int port = Integer.parseInt(ip[ip.length-1]);
                        String host = String.join(":", Arrays.copyOfRange(ip, 0, ip.length-1));
                        if (host.startsWith("[") && host.endsWith("]")) //tcp6 in [address]:port format
                            host = host.substring(1, host.length() - 1);

						Socket client_socket = new Socket(host, port);
                        
						PrintWriter writer = new PrintWriter(client_socket.getOutputStream(),true);
						connections.put(target_ip,writer);
						System.out.println("Connection for forwarding events to " + target_ip + " established");
					}
					connections.get(target_ip).println(event.toString());
				}
				catch(Exception e)
				{
                    
					System.err.println("Something: "+e.toString() + " - Event:" + event + " to " + target_ip);
				}
			}

			private Map<String,PrintWriter> connections = new HashMap<String,PrintWriter>();
	    });
        // Start cluster/CEP-engine
		env.execute("Flink Java API Skeleton");
	}
}
