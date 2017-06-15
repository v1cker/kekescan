# -*- coding: utf-8 -*-  
# code by evileo



from celery import task, platforms
from celery import Celery
import subprocess
from subprocess import Popen,PIPE
import re
import json

import gevent
from gevent.pool import Pool
from app.lib.utils import *
from app.lib.crawler import MyCrawler, similarity
from bugscan.poc_launcher import Poc_Launcher
from celery import task
from app.models import Req_list
from urlparse import urlparse
from os import path

bugscan_name_list = ['a_test.py','exp_103.py','exp_104.py','exp_1046.py','exp_105.py','exp_1050.py','exp_1051.py','exp_1052.py','exp_1058.py','exp_106.py','exp_1060.py','exp_1061.py','exp_1063.py','exp_1067.py','exp_1068.py','exp_1069.py','exp_107.py','exp_1072.py','exp_1073.py','exp_1074.py','exp_1076.py','exp_108.py','exp_1082.py','exp_1083.py','exp_1102.py','exp_1103.py','exp_1104.py','exp_1105.py','exp_1107.py','exp_1108.py','exp_1109.py','exp_1111.py','exp_1113.py','exp_1114.py','exp_1118.py','exp_1119.py','exp_1121.py','exp_1122.py','exp_1123.py','exp_1124.py','exp_1125.py','exp_1126.py','exp_1127.py','exp_113.py','exp_1130.py','exp_1132.py','exp_1136.py','exp_1138.py','exp_1139.py','exp_1140.py','exp_1141.py','exp_1143.py','exp_1144.py','exp_1146.py','exp_1148.py','exp_1149.py','exp_1150.py','exp_1151.py','exp_1152.py','exp_1153.py','exp_1160.py','exp_1161.py','exp_1162.py','exp_1164.py','exp_1165.py','exp_1168.py','exp_1169.py','exp_1170.py','exp_1171.py','exp_1172.py','exp_1176.py','exp_1177.py','exp_1179.py','exp_118.py','exp_1182.py','exp_1183.py','exp_1185.py','exp_1186.py','exp_1189.py','exp_1190.py','exp_1192.py','exp_1193.py','exp_1194.py','exp_1195.py','exp_1199.py','exp_120.py','exp_1200.py','exp_1201.py','exp_1202.py','exp_1203.py','exp_1204.py','exp_1218.py','exp_1219.py','exp_1223.py','exp_1224.py','exp_1225.py','exp_1226.py','exp_1227.py','exp_1228.py','exp_1230.py','exp_1231.py','exp_1232.py','exp_1233.py','exp_1235.py','exp_1236.py','exp_1237.py','exp_1238.py','exp_1252.py','exp_1253.py','exp_1254.py','exp_1255.py','exp_1257.py','exp_1258.py','exp_1260.py','exp_1262.py','exp_1263.py','exp_1264.py','exp_1267.py','exp_1268.py','exp_127.py','exp_1271.py','exp_1272.py','exp_1273.py','exp_1274.py','exp_1275.py','exp_1276.py','exp_1277.py','exp_1278.py','exp_1279.py','exp_128.py','exp_1280.py','exp_1283.py','exp_1284.py','exp_1285.py','exp_1286.py','exp_1288.py','exp_1289.py','exp_129.py','exp_1290.py','exp_1292.py','exp_130.py','exp_1300.py','exp_1303.py','exp_1304.py','exp_131.py','exp_1323.py','exp_1328.py','exp_133.py','exp_1332.py','exp_1335.py','exp_1336.py','exp_1339.py','exp_134.py','exp_1340.py','exp_1341.py','exp_1344.py','exp_1349.py','exp_1351.py','exp_1352.py','exp_1354.py','exp_1356.py','exp_1358.py','exp_1359.py','exp_1363.py','exp_1364.py','exp_1365.py','exp_1368.py','exp_1376.py','exp_138.py','exp_139.py','exp_1393.py','exp_140.py','exp_1406.py','exp_1408.py','exp_141.py','exp_1412.py','exp_1417.py','exp_1418.py','exp_1419.py','exp_142.py','exp_1422.py','exp_1424.py','exp_143.py','exp_1435.py','exp_1437.py','exp_1438.py','exp_144.py','exp_1441.py','exp_1442.py','exp_1447.py','exp_1448.py','exp_1449.py','exp_1454.py','exp_1457.py','exp_1461.py','exp_1463.py','exp_1466.py','exp_147.py','exp_1470.py','exp_1473.py','exp_1475.py','exp_1476.py','exp_1479.py','exp_1481.py','exp_1483.py','exp_1484.py','exp_1485.py','exp_1489.py','exp_1490.py','exp_1492.py','exp_1494.py','exp_1497.py','exp_1502.py','exp_1503.py','exp_1507.py','exp_152.py','exp_1521.py','exp_1525.py','exp_1526.py','exp_1530.py','exp_1545.py','exp_155.py','exp_1553.py','exp_1556.py','exp_1559.py','exp_156.py','exp_1561.py','exp_157.py','exp_158.py','exp_1582.py','exp_159.py','exp_1592.py','exp_1595.py','exp_1597.py','exp_160.py','exp_1604.py','exp_1606.py','exp_161.py','exp_1616.py','exp_162.py','exp_1626.py','exp_1628.py','exp_1629.py','exp_163.py','exp_1633.py','exp_1634.py','exp_1635.py','exp_1637.py','exp_1639.py','exp_164.py','exp_1644.py','exp_1645.py','exp_1646.py','exp_1647.py','exp_1655.py','exp_1656.py','exp_1657.py','exp_166.py','exp_1662.py','exp_1664.py','exp_1666.py','exp_1667.py','exp_1668.py','exp_167.py','exp_1670.py','exp_1671.py','exp_1672.py','exp_1674.py','exp_1675.py','exp_1676.py','exp_1677.py','exp_168.py','exp_1680.py','exp_1681.py','exp_1687.py','exp_169.py','exp_1690.py','exp_1692.py','exp_1693.py','exp_1697.py','exp_170.py','exp_1702.py','exp_1704.py','exp_1706.py','exp_1707.py','exp_1709.py','exp_171.py','exp_1710.py','exp_1713.py','exp_1715.py','exp_1717.py','exp_1718.py','exp_172.py','exp_1721.py','exp_1723.py','exp_1725.py','exp_1739.py','exp_174.py','exp_1740.py','exp_1741.py','exp_1742.py','exp_1744.py','exp_1746.py','exp_1748.py','exp_1749.py','exp_175.py','exp_1750.py','exp_1753.py','exp_1754.py','exp_1755.py','exp_1757.py','exp_176.py','exp_1769.py','exp_177.py','exp_1770.py','exp_1773.py','exp_1774.py','exp_1775.py','exp_1776.py','exp_1777.py','exp_1778.py','exp_1779.py','exp_1780.py','exp_1781.py','exp_1783.py','exp_1784.py','exp_1785.py','exp_1788.py','exp_179.py','exp_1791.py','exp_1792.py','exp_1793.py','exp_1796.py','exp_1797.py','exp_1798.py','exp_1799.py','exp_1801.py','exp_1805.py','exp_1806.py','exp_1807.py','exp_181.py','exp_1810.py','exp_1814.py','exp_1815.py','exp_1816.py','exp_1817.py','exp_1818.py','exp_1819.py','exp_182.py','exp_1821.py','exp_1822.py','exp_1823.py','exp_1824.py','exp_1826.py','exp_1827.py','exp_1828.py','exp_1829.py','exp_1831.py','exp_1832.py','exp_1833.py','exp_1834.py','exp_1835.py','exp_1836.py','exp_1837.py','exp_1838.py','exp_184.py','exp_1846.py','exp_1847.py','exp_1848.py','exp_1849.py','exp_1852.py','exp_1853.py','exp_1861.py','exp_1862.py','exp_1863.py','exp_1864.py','exp_1865.py','exp_1866.py','exp_1868.py','exp_1871.py','exp_1872.py','exp_1874.py','exp_1875.py','exp_1879.py','exp_1880.py','exp_1881.py','exp_1885.py','exp_1888.py','exp_1889.py','exp_1891.py','exp_1894.py','exp_1896.py','exp_1897.py','exp_1898.py','exp_1901.py','exp_1902.py','exp_1903.py','exp_1906.py','exp_1909.py','exp_1910.py','exp_1912.py','exp_1913.py','exp_1914.py','exp_1915.py','exp_1917.py','exp_1918.py','exp_1919.py','exp_1920.py','exp_1921.py','exp_1922.py','exp_1924.py','exp_1925.py','exp_1926.py','exp_1927.py','exp_1928.py','exp_193.py','exp_1930.py','exp_1933.py','exp_1934.py','exp_1936.py','exp_1937.py','exp_1939.py','exp_1941.py','exp_1942.py','exp_1943.py','exp_1944.py','exp_1945.py','exp_1946.py','exp_1947.py','exp_1948.py','exp_195.py','exp_1950.py','exp_1951.py','exp_1952.py','exp_1953.py','exp_1954.py','exp_1956.py','exp_1957.py','exp_1959.py','exp_1961.py','exp_1962.py','exp_1963.py','exp_1965.py','exp_1966.py','exp_1967.py','exp_1968.py','exp_1969.py','exp_1970.py','exp_1974.py','exp_1977.py','exp_1978.py','exp_1979.py','exp_1981.py','exp_1982.py','exp_1984.py','exp_1985.py','exp_1986.py','exp_1987.py','exp_1988.py','exp_1989.py','exp_1990.py','exp_1993.py','exp_1996.py','exp_1997.py','exp_1998.py','exp_1999.py','exp_200.py','exp_2000.py','exp_2001.py','exp_2002.py','exp_2003.py','exp_2004.py','exp_2005.py','exp_2007.py','exp_2008.py','exp_2009.py','exp_2010.py','exp_2011.py','exp_2016.py','exp_2019.py','exp_202.py','exp_2020.py','exp_2021.py','exp_2022.py','exp_2024.py','exp_2025.py','exp_2026.py','exp_2029.py','exp_2031.py','exp_2032.py','exp_2033.py','exp_2034.py','exp_2035.py','exp_2038.py','exp_204.py','exp_2041.py','exp_2042.py','exp_2043.py','exp_2044.py','exp_2047.py','exp_2049.py','exp_205.py','exp_2050.py','exp_2051.py','exp_2052.py','exp_2054.py','exp_2069.py','exp_2070.py','exp_2071.py','exp_2074.py','exp_2075.py','exp_2077.py','exp_2079.py','exp_208.py','exp_2080.py','exp_2084.py','exp_2089.py','exp_2091.py','exp_2092.py','exp_2094.py','exp_2097.py','exp_2098.py','exp_2099.py','exp_2100.py','exp_2101.py','exp_2104.py','exp_2105.py','exp_2106.py','exp_2107.py','exp_2108.py','exp_2109.py','exp_2114.py','exp_2115.py','exp_2116.py','exp_2117.py','exp_2119.py','exp_2130.py','exp_2132.py','exp_2134.py','exp_2136.py','exp_2138.py','exp_2139.py','exp_2140.py','exp_2143.py','exp_2144.py','exp_2146.py','exp_2149.py','exp_2151.py','exp_2153.py','exp_2155.py','exp_2158.py','exp_2159.py','exp_2160.py','exp_2161.py','exp_2162.py','exp_2163.py','exp_2164.py','exp_2166.py','exp_2170.py','exp_2171.py','exp_2173.py','exp_2174.py','exp_2178.py','exp_2183.py','exp_2184.py','exp_2185.py','exp_2188.py','exp_2189.py','exp_219.py','exp_2193.py','exp_2194.py','exp_2195.py','exp_2196.py','exp_2197.py','exp_2198.py','exp_220.py','exp_2201.py','exp_2202.py','exp_2203.py','exp_2204.py','exp_2205.py','exp_2206.py','exp_2210.py','exp_2212.py','exp_2215.py','exp_2216.py','exp_2219.py','exp_2220.py','exp_2228.py','exp_2229.py','exp_2230.py','exp_2231.py','exp_2232.py','exp_2234.py','exp_2236.py','exp_2237.py','exp_2238.py','exp_2241.py','exp_2242.py','exp_2243.py','exp_2244.py','exp_2245.py','exp_2248.py','exp_2250.py','exp_2251.py','exp_2252.py','exp_2253.py','exp_2262.py','exp_2269.py','exp_2272.py','exp_2274.py','exp_2282.py','exp_2283.py','exp_2284.py','exp_2285.py','exp_2286.py','exp_2287.py','exp_2288.py','exp_2289.py','exp_2291.py','exp_2294.py','exp_2295.py','exp_2296.py','exp_2297.py','exp_2298.py','exp_2299.py','exp_2301.py','exp_2302.py','exp_2303.py','exp_2305.py','exp_2306.py','exp_2307.py','exp_2308.py','exp_2309.py','exp_2310.py','exp_2311.py','exp_2312.py','exp_2313.py','exp_2314.py','exp_2315.py','exp_2316.py','exp_2317.py','exp_2318.py','exp_2320.py','exp_2321.py','exp_2322.py','exp_2337.py','exp_2338.py','exp_2339.py','exp_234.py','exp_2340.py','exp_2341.py','exp_2342.py','exp_2343.py','exp_2345.py','exp_2346.py','exp_2347.py','exp_2348.py','exp_2350.py','exp_2351.py','exp_2353.py','exp_2354.py','exp_2355.py','exp_2357.py','exp_236.py','exp_2361.py','exp_2362.py','exp_2363.py','exp_2365.py','exp_2366.py','exp_2367.py','exp_2369.py','exp_237.py','exp_2370.py','exp_2371.py','exp_2372.py','exp_2373.py','exp_2374.py','exp_2375.py','exp_2376.py','exp_2377.py','exp_2378.py','exp_2379.py','exp_238.py','exp_2380.py','exp_2381.py','exp_2382.py','exp_2383.py','exp_2384.py','exp_2385.py','exp_2386.py','exp_2387.py','exp_2388.py','exp_2390.py','exp_2391.py','exp_2392.py','exp_2393.py','exp_2394.py','exp_2395.py','exp_240.py','exp_2403.py','exp_2405.py','exp_2406.py','exp_2408.py','exp_241.py','exp_2419.py','exp_2420.py','exp_2421.py','exp_2422.py','exp_2423.py','exp_2424.py','exp_2425.py','exp_2426.py','exp_2431.py','exp_2439.py','exp_2441.py','exp_2442.py','exp_2443.py','exp_2446.py','exp_2453.py','exp_2455.py','exp_2456.py','exp_2457.py','exp_2458.py','exp_2459.py','exp_246.py','exp_2462.py','exp_2467.py','exp_2469.py','exp_2471.py','exp_2473.py','exp_2474.py','exp_2477.py','exp_2478.py','exp_2482.py','exp_2488.py','exp_2492.py','exp_2493.py','exp_2494.py','exp_2495.py','exp_2496.py','exp_2498.py','exp_2499.py','exp_250.py','exp_2500.py','exp_2502.py','exp_2506.py','exp_251.py','exp_2517.py','exp_2518.py','exp_2522.py','exp_2528.py','exp_2529.py','exp_253.py','exp_2534.py','exp_2539.py','exp_254.py','exp_2542.py','exp_2544.py','exp_2547.py','exp_2548.py','exp_2549.py','exp_255.py','exp_2550.py','exp_2551.py','exp_2552.py','exp_2553.py','exp_2554.py','exp_2555.py','exp_2556.py','exp_2557.py','exp_2559.py','exp_2562.py','exp_2563.py','exp_2564.py','exp_2565.py','exp_2566.py','exp_2567.py','exp_2568.py','exp_2570.py','exp_2571.py','exp_2572.py','exp_2575.py','exp_2576.py','exp_2578.py','exp_2580.py','exp_2581.py','exp_2583.py','exp_2586.py','exp_2588.py','exp_2589.py','exp_2590.py','exp_2591.py','exp_2592.py','exp_2593.py','exp_2594.py','exp_2595.py','exp_2597.py','exp_2598.py','exp_2599.py','exp_2603.py','exp_2604.py','exp_2605.py','exp_2606.py','exp_2607.py','exp_2609.py','exp_261.py','exp_2610.py','exp_2611.py','exp_2612.py','exp_2613.py','exp_2614.py','exp_2616.py','exp_2617.py','exp_2618.py','exp_2619.py','exp_2620.py','exp_2621.py','exp_2622.py','exp_2623.py','exp_2624.py','exp_2625.py','exp_2627.py','exp_2628.py','exp_2629.py','exp_263.py','exp_2631.py','exp_2632.py','exp_2633.py','exp_2634.py','exp_2635.py','exp_2636.py','exp_2639.py','exp_2640.py','exp_2641.py','exp_2642.py','exp_2643.py','exp_2645.py','exp_2647.py','exp_2648.py','exp_2650.py','exp_2654.py','exp_2655.py','exp_2656.py','exp_2658.py','exp_2659.py','exp_266.py','exp_2660.py','exp_2661.py','exp_2663.py','exp_2667.py','exp_2668.py','exp_267.py','exp_2670.py','exp_2671.py','exp_2672.py','exp_2673.py','exp_2675.py','exp_2676.py','exp_2678.py','exp_2679.py','exp_2681.py','exp_2682.py','exp_2683.py','exp_2684.py','exp_2685.py','exp_2686.py','exp_2687.py','exp_2688.py','exp_2689.py','exp_2690.py','exp_2691.py','exp_2692.py','exp_2693.py','exp_2696.py','exp_2697.py','exp_2699.py','exp_2700.py','exp_2701.py','exp_2702.py','exp_2703.py','exp_2705.py','exp_2706.py','exp_2707.py','exp_2708.py','exp_2709.py','exp_2710.py','exp_2711.py','exp_2712.py','exp_2713.py','exp_2714.py','exp_2715.py','exp_2716.py','exp_2717.py','exp_2718.py','exp_2719.py','exp_2720.py','exp_2722.py','exp_2723.py','exp_2724.py','exp_2726.py','exp_2727.py','exp_2729.py','exp_2730.py','exp_2731.py','exp_2732.py','exp_2733.py','exp_2734.py','exp_2735.py','exp_2737.py','exp_2738.py','exp_2739.py','exp_274.py','exp_2740.py','exp_2741.py','exp_2742.py','exp_2744.py','exp_2745.py','exp_2746.py','exp_2748.py','exp_2751.py','exp_2752.py','exp_2753.py','exp_2760.py','exp_2762.py','exp_2763.py','exp_2764.py','exp_2765.py','exp_2766.py','exp_2767.py','exp_2768.py','exp_2770.py','exp_2771.py','exp_2775.py','exp_2776.py','exp_2777.py','exp_2778.py','exp_278.py','exp_2780.py','exp_2781.py','exp_2782.py','exp_2783.py','exp_2784.py','exp_2787.py','exp_2788.py','exp_2794.py','exp_2798.py','exp_2799.py','exp_2801.py','exp_2802.py','exp_2803.py','exp_2809.py','exp_2820.py','exp_2821.py','exp_284.py','exp_285.py','exp_287.py','exp_289.py','exp_290.py','exp_291.py','exp_293.py','exp_294.py','exp_297.py','exp_298.py','exp_299.py','exp_302.py','exp_303.py','exp_304.py','exp_307.py','exp_314.py','exp_315.py','exp_317.py','exp_319.py','exp_321.py','exp_324.py','exp_333.py','exp_337.py','exp_342.py','exp_343.py','exp_344.py','exp_345.py','exp_346.py','exp_347.py','exp_349.py','exp_351.py','exp_356.py','exp_361.py','exp_363.py','exp_373.py','exp_374.py','exp_376.py','exp_377.py','exp_379.py','exp_383.py','exp_384.py','exp_385.py','exp_386.py','exp_387.py','exp_388.py','exp_389.py','exp_390.py','exp_391.py','exp_392.py','exp_394.py','exp_395.py','exp_397.py','exp_398.py','exp_4.py','exp_401.py','exp_407.py','exp_408.py','exp_41.py','exp_411.py','exp_412.py','exp_414.py','exp_417.py','exp_418.py','exp_419.py','exp_420.py','exp_421.py','exp_422.py','exp_427.py','exp_428.py','exp_431.py','exp_432.py','exp_433.py','exp_434.py','exp_436.py','exp_439.py','exp_440.py','exp_442.py','exp_443.py','exp_445.py','exp_448.py','exp_449.py','exp_450.py','exp_456.py','exp_465.py','exp_466.py','exp_467.py','exp_469.py','exp_47.py','exp_470.py','exp_471.py','exp_473.py','exp_474.py','exp_475.py','exp_478.py','exp_479.py','exp_480.py','exp_481.py','exp_482.py','exp_483.py','exp_484.py','exp_485.py','exp_486.py','exp_488.py','exp_489.py','exp_490.py','exp_491.py','exp_495.py','exp_501.py','exp_502.py','exp_509.py','exp_510.py','exp_511.py','exp_512.py','exp_52.py','exp_521.py','exp_528.py','exp_529.py','exp_53.py','exp_530.py','exp_543.py','exp_546.py','exp_554.py','exp_555.py','exp_557.py','exp_558.py','exp_559.py','exp_56.py','exp_560.py','exp_561.py','exp_562.py','exp_564.py','exp_570.py','exp_572.py','exp_574.py','exp_576.py','exp_580.py','exp_586.py','exp_588.py','exp_590.py','exp_592.py','exp_593.py','exp_594.py','exp_595.py','exp_596.py','exp_600.py','exp_602.py','exp_606.py','exp_607.py','exp_609.py','exp_612.py','exp_613.py','exp_616.py','exp_617.py','exp_619.py','exp_622.py','exp_623.py','exp_624.py','exp_631.py','exp_640.py','exp_657.py','exp_67.py','exp_679.py','exp_68.py','exp_682.py','exp_683.py','exp_685.py','exp_687.py','exp_688.py','exp_689.py','exp_69.py','exp_690.py','exp_695.py','exp_697.py','exp_701.py','exp_702.py','exp_727.py','exp_732.py','exp_733.py','exp_739.py','exp_740.py','exp_744.py','exp_745.py','exp_746.py','exp_747.py','exp_748.py','exp_749.py','exp_750.py','exp_753.py','exp_755.py','exp_756.py','exp_758.py','exp_759.py','exp_761.py','exp_773.py','exp_777.py','exp_779.py','exp_78.py','exp_785.py','exp_788.py','exp_790.py','exp_793.py','exp_80.py','exp_802.py','exp_803.py','exp_804.py','exp_806.py','exp_807.py','exp_808.py','exp_81.py','exp_815.py','exp_817.py','exp_821.py','exp_823.py','exp_826.py','exp_827.py','exp_828.py','exp_830.py','exp_831.py','exp_832.py','exp_834.py','exp_837.py','exp_838.py','exp_839.py','exp_840.py','exp_841.py','exp_842.py','exp_843.py','exp_847.py','exp_848.py','exp_849.py','exp_850.py','exp_851.py','exp_852.py','exp_853.py','exp_854.py','exp_856.py','exp_858.py','exp_860.py','exp_861.py','exp_862.py','exp_864.py','exp_865.py','exp_867.py','exp_868.py','exp_869.py','exp_875.py','exp_876.py','exp_877.py','exp_878.py','exp_885.py','exp_887.py','exp_889.py','exp_890.py','exp_893.py','exp_895.py','exp_899.py','exp_901.py','exp_929.py','exp_930.py','exp_931.py','exp_946.py','exp_948.py','exp_951.py','exp_954.py','exp_955.py','exp_956.py','exp_957.py','exp_97.py','exp_99.py','exp_back_100.py','exp_back_101.py','exp_back_102.py','exp_back_1054.py','exp_back_1055.py','exp_back_1056.py','exp_back_1062.py','exp_back_1070.py','exp_back_1071.py','exp_back_11.py','exp_back_12.py','exp_back_13.py','exp_back_15.py','exp_back_16.py','exp_back_17.py','exp_back_1745.py','exp_back_1756.py','exp_back_1766.py','exp_back_1782.py','exp_back_1786.py','exp_back_18.py','exp_back_189.py','exp_back_19.py','exp_back_1994.py','exp_back_1995.py','exp_back_20.py','exp_back_2065.py','exp_back_2066.py','exp_back_2067.py','exp_back_2078.py','exp_back_2083.py','exp_back_2110.py','exp_back_2112.py','exp_back_22.py','exp_back_23.py','exp_back_24.py','exp_back_25.py','exp_back_26.py','exp_back_27.py','exp_back_28.py','exp_back_29.py','exp_back_30.py','exp_back_33.py','exp_back_34.py','exp_back_35.py','exp_back_36.py','exp_back_37.py','exp_back_38.py','exp_back_39.py','exp_back_45.py','exp_back_46.py','exp_back_54.py','exp_back_57.py','exp_back_58.py','exp_back_59.py','exp_back_6.py','exp_back_60.py','exp_back_61.py','exp_back_62.py','exp_back_63.py','exp_back_64.py','exp_back_641.py','exp_back_65.py','exp_back_7.py','exp_back_70.py','exp_back_71.py','exp_back_72.py','exp_back_73.py','exp_back_74.py','exp_back_75.py','exp_back_76.py','exp_back_77.py','exp_back_8.py','exp_back_811.py','exp_back_82.py','exp_back_83.py','exp_back_84.py','exp_back_85.py','exp_back_86.py','exp_back_87.py','exp_back_88.py','exp_back_89.py','exp_back_9.py','exp_back_953.py','exp_back_98.py']

TASKS_ROOT = path.dirname(path.abspath(path.dirname(__file__)))


celery_app = Celery()

# 允许celery以root权限启动
platforms.C_FORCE_ROOT = True

# 修改celery的全局配置
celery_app.conf.update(
    CELERY_IMPORTS = ("app.tasks", ),
    #BROKER_URL = 'redis://:ruijiangmei@115.28.72.96:6379/1',
    #CELERY_RESULT_BACKEND = 'redis://:ruijiangmei@115.28.72.96:6379/1',
    BROKER_URL = 'redis://localhost:6379/0',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0',
    #CELERY_RESULT_BACKEND = 'db+mysql://root:wenjunnengyoujiduochou@127.0.0.1:3306/xlcscan',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}, # 如果任务没有在 可见性超时 内确认接收，任务会被重新委派给另一个Worker并执行  默认1 hour.
    CELERYD_CONCURRENCY = 50 ,
    CELERY_TASK_RESULT_EXPIRES = 1200,  # celery任务执行结果的超时时间，我的任务都不需要返回结
    # BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True},       # 设置一个传输选项来给消息加上前缀
)


 
@celery_app.task(time_limit=3600)
def run_fnascan(target):     
    fnascan_workspace =   path.join(TASKS_ROOT, 'tools','FNAScan').replace('\\', '/')
    #"D:/Projects/xlcscan/xlcscan/tools/FNAScan/"
    #print fnascan_workspace
    cmd = 'python F-NAScan.kscan.py -h %s' % target #221.226.15.243-221.226.15.245 , 221.226.15.243,221.226.15.245
    p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ,cwd=fnascan_workspace,)  
    process_output = p.stdout.readlines()
    return process_output   

# @celery_app.task(time_limit=3600)
# def run_bugscan(url_list):     
#     from tools.pocs.bugscan import Bugscan
#     PLUGINS_DIR = 'D:\\Projects\\xlcscan\\tools\\pocs\\'
#     poc = Bugscan()
#     pool = Pool(100)
#     for target in url_list: 
#         for poc_file in bugscan_name_list:
#             if target and poc_file:
#                 target = fix_target(target)
#                 poc_file = PLUGINS_DIR + 'bugscan' + '\\' + poc_file
#                 pool.add(gevent.spawn(poc.run, target,poc_file))
#     pool.join()

    
@celery_app.task(time_limit=3600)
def run_subdomainbrute(target):     
    subdomainbrute_workspace = path.join(TASKS_ROOT, 'tools','subDomainsBrute').replace('\\', '/')  
    cmd = 'subDomainsBrute.py %s -f  dict/test_subnames.txt' % target # 
    p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ,cwd=subdomainbrute_workspace,)  
    process_output = p.stdout.readlines()
    return process_output   


# 失败任务重启休眠时间300秒，最大重试次数5次
# @app.task(bind=True, default_retry_delay=300, max_retries=5)
@task(time_limit=3600)
def run_task_in_gevent(url_list, poc_file_dict):  # url_list 每个进程分配到一定量的url
    poc = Poc_Launcher()
    pool = Pool(100)
    for target in url_list:
        for plugin_type, poc_files in poc_file_dict.iteritems():
            for poc_file in poc_files:
                if target and poc_file:
                    target = fix_target(target)
                    pool.add(gevent.spawn(poc.poc_verify, target, plugin_type, poc_file))
    pool.join()


@task(time_limit=3600)
def crawler(target, cookie, ua):
    result = {}
    crawl_count = 5
    craw = MyCrawler(target, cookie, ua)
    craw.crawling(target, crawl_count)
    url_list = list(set(craw.linkQuence.getUnvisitedUrl() + craw.linkQuence.getVisitedUrl()))
    size = 1000000000
    for url in url_list:
        try:
            temp = {str(similarity(url, size)): url}
            result.update(temp)
        except Exception, e:
            print e
    try:
        for url in result.values():
            tmp = urlparse(url)
            Req_list(method="GET",
                     host=tmp.netloc,
                     uri=tmp.path,
                     url=url.encode("utf8"),
                     ua=ua,
                     cookie=cookie,
                     ).save()
    except Exception, e:
        pass
    return result

import time   
@celery_app.task(time_limit=3600)
def add(s):
    s = s.split(',')
    #print x * y
    time.sleep(10)
    return s[0] + s[1] 
    
