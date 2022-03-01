using System;

namespace DCEP.Core
{
    public enum TimeUnit
    {
        Second,
        Minute,
        Hour
    }

    public static class TimeUnitHelper
    {
        public static TimeSpan GetTimeSpanFromDuration(this TimeUnit timeUnit, double duration)
        {
            switch (timeUnit)
            {
                case TimeUnit.Second:
                    return TimeSpan.FromSeconds(duration);

                case TimeUnit.Minute:
                    return TimeSpan.FromMinutes(duration);

                case TimeUnit.Hour:
                    return TimeSpan.FromHours(duration);

                default:
                    throw new ArgumentException("Invalid TimeUnit in TimeUnitHelper.GetTimeSpan");
            }
        }

        public static TimeSpan GetIntervalFromCountPerUnit(this TimeUnit timeUnit, int eventCount)
        {
            return timeUnit.GetTimeSpanFromDuration(1.0 / eventCount);
        }


    }

}