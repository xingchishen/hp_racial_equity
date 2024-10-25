cd "C:\Users\wills\Dropbox (YSE)\xingchi.shen@yale.edu's files\heating equity"

import delimited "data\Analysis\households_9ST2021_withinRedliningMap.csv", case(preserve) 

gen Category=1 if category=="Best"
replace Category=2 if category=="Still Desirable"
replace Category=3 if category=="Definitely Declining"
replace Category=4 if category=="Hazardous"
egen city_id=group(city state)


areg Ethnic3 Category, absorb(city_id)
******************************************************************************
Linear regression, absorbing indicators          Number of obs     = 1,684,756
Absorbed variable: city_id                       No. of categories =        66
                                                 F(1, 1684689)     =  15281.73
                                                 Prob > F          =    0.0000
                                                 R-squared         =    0.1804
                                                 Adj R-squared     =    0.1804
                                                 Root MSE          =    0.4398

------------------------------------------------------------------------------
     Ethnic3 | Coefficient  Std. err.      t    P>|t|     [95% conf. interval]
-------------+----------------------------------------------------------------
    Category |   -.052308   .0004231  -123.62   0.000    -.0531374   -.0514787
       _cons |    .763479    .001223   624.25   0.000     .7610818    .7658761
------------------------------------------------------------------------------
F test of absorbed indicators: F(65, 1684689) = 5127.312      Prob > F = 0.000
******************************************************************************



areg building_age Category, absorb(city_id)
******************************************************************************
Linear regression, absorbing indicators          Number of obs     = 1,626,351
Absorbed variable: city_id                       No. of categories =        66
                                                 F(1, 1626284)     =   9520.18
                                                 Prob > F          =    0.0000
                                                 R-squared         =    0.0900
                                                 Adj R-squared     =    0.0899
                                                 Root MSE          =   29.5426

------------------------------------------------------------------------------
building_age | Coefficient  Std. err.      t    P>|t|     [95% conf. interval]
-------------+----------------------------------------------------------------
    Category |   2.826989   .0289735    97.57   0.000     2.770202    2.883776
       _cons |   81.34036   .0834811   974.36   0.000     81.17674    81.50398
------------------------------------------------------------------------------
F test of absorbed indicators: F(65, 1626284) = 2291.541      Prob > F = 0.000
******************************************************************************


areg building_age Category FIND_DIV_1000, absorb(city_id)
******************************************************************************
Linear regression, absorbing indicators          Number of obs     = 1,626,351
Absorbed variable: city_id                       No. of categories =        66
                                                 F(2, 1626283)     =   6565.94
                                                 Prob > F          =    0.0000
                                                 R-squared         =    0.0920
                                                 Adj R-squared     =    0.0919
                                                 Root MSE          =   29.5101

-------------------------------------------------------------------------------
 building_age | Coefficient  Std. err.      t    P>|t|     [95% conf. interval]
--------------+----------------------------------------------------------------
     Category |   2.281504   .0303395    75.20   0.000     2.222039    2.340968
FIND_DIV_1000 |  -.0242659    .000405   -59.92   0.000    -.0250596   -.0234722
        _cons |   84.48106   .0984929   857.74   0.000     84.28801     84.6741
-------------------------------------------------------------------------------
F test of absorbed indicators: F(65, 1626283) = 2304.552      Prob > F = 0.000
******************************************************************************



areg building_age Category WEALTH_FINDER_SCORE , absorb(city_id)
******************************************************************************
Linear regression, absorbing indicators          Number of obs     = 1,626,351
Absorbed variable: city_id                       No. of categories =        66
                                                 F(2, 1626283)     =  15254.47
                                                 Prob > F          =    0.0000
                                                 R-squared         =    0.1015
                                                 Adj R-squared     =    0.1015
                                                 Root MSE          =   29.3549

-------------------------------------------------------------------------------------
       building_age | Coefficient  Std. err.      t    P>|t|     [95% conf. interval]
--------------------+----------------------------------------------------------------
           Category |   1.272809   .0307342    41.41   0.000     1.212571    1.333047
WEALTH_FINDER_SCORE |  -.0051245   .0000355  -144.45   0.000     -.005194   -.0050549
              _cons |   93.08025   .1161286   801.53   0.000     92.85264    93.30785
-------------------------------------------------------------------------------------
F test of absorbed indicators: F(65, 1626283) = 2397.334      Prob > F = 0.000
******************************************************************************
