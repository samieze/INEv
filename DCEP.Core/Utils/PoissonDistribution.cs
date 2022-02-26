using System;

namespace DCEP.Core.Utils.PoissonEvaluator
{
    // Implementation of the Poisson Cumulative Distribution function for large Lambdas
    // code from https://www.codeproject.com/Tips/1216237/Csharp-Poisson-Cumulative-Distribution-for-large-L
    // licensed under The Code Project Open License (CPOL)
    public class PoissonDistribution
    {
        private readonly double _lambda;

        public PoissonDistribution(double lambda = 1.0)
        {
            _lambda = lambda;
        }

        public double Pmf(long k)
        {
            if (k > 170 || double.IsInfinity(Math.Pow(_lambda, k)))
            {
                var logLambda = k * Math.Log(_lambda) - _lambda - (k * Math.Log(k) -
                    k + Math.Log(k * (1 + 4 * k * (1 + 2 * k))) / 6 + Math.Log(Math.PI) / 2);
                return Math.Pow(Math.E, logLambda);
            }
            return Math.Pow(Math.E, -_lambda) * Math.Pow(_lambda, k) / Factorial(k);
        }

        public double Cdf(long k)
        {
            long i = 0;
            var sum = 0.0;
            var infinityIsFound = false;
            var eLambda = Math.Pow(Math.E, -_lambda);
            var logPiDivTwo = Math.Log(Math.PI) / 2;
            while (i <= k)
            {
                double n;
                if (infinityIsFound)
                {
                    var log6ThTail = Math.Log(i * (1 + 4 * i * (1 + 2 * i))) / 6;
                    var lnN = i * Math.Log(_lambda) - (i * Math.Log(i) - i + log6ThTail + logPiDivTwo);
                    n = Math.Pow(Math.E, lnN - _lambda);
                }
                else
                {
                    if (i > 170 || double.IsInfinity(Math.Pow(_lambda, i)))
                    {
                        infinityIsFound = true;
                        var log6ThTail = Math.Log(i * (1 + 4 * i * (1 + 2 * i))) / 6;
                        var lnN = i * Math.Log(_lambda) - (i * Math.Log(i) - i + log6ThTail + logPiDivTwo);
                        n = Math.Pow(Math.E, lnN - _lambda);
                    }
                    else
                    {
                        n = eLambda * Math.Pow(_lambda, i) / Factorial(i);
                    }
                }

                sum += n;
                i++;
            }
            return (sum > 1) ? 1.0 : sum;
        }


        public double Cdf0(long k)
        {
            var e = Math.Pow(Math.E, -_lambda);
            long i = 0;
            var sum = 0.0;
            while (i <= k)
            {
                sum += e * Math.Pow(_lambda, i) / Factorial(i);
                i++;
            }
            return sum;
        }

        public double Cdf1(long k)
        {
            var e = Math.Pow(Math.E, -_lambda);
            long i = 0;
            var sum = 0.0;
            while (i <= k)
            {
                sum += Pmf(i);
                i++;
            }
            return sum;
        }

        public double Factorial(long k)
        {
            long count = k;
            double factorial = 1;
            while (count >= 1)
            {
                factorial = factorial * count;
                count--;
            }

            return factorial;
        }


        //https://en.wikipedia.org/wiki/Factorial
        //https://sv.wikipedia.org/wiki/Stirlings_formel
        public double Factorial1(long k)
        {
            //Srinivasa Ramanujan (Ramanujan 1988)
            return Math.Round(Math.Pow(Math.E, k * Math.Log(k) - k +
                Math.Log(k * (1 + 4 * k * (1 + 2 * k))) / 6 + Math.Log(Math.PI) / 2));
        }

        public double Factorial12(double k)
        {
            var factorial = Math.Sqrt((2 * k + 1.0 / 3) * Math.PI) * Math.Pow(k, k) * Math.Pow(Math.E, -k);
            return factorial;
        }

        public double Factorial3(long k)
        {
            //Srinivasa Ramanujan (Ramanujan 1988) .

            var c1 = Math.Sqrt(2 * Math.PI * k) * Math.Pow(k / Math.E, k);
            return c1 * Math.Round(Math.Pow(Math.E, 1.0 / (12 * k) - 1.0 / (360 * Math.Pow(k, 3) + 1.0 / (20160 * Math.Pow(k, 5)) - 1.0 / (1814400 * Math.Pow(k, 7)))));
        }
    }
}
