////////// Use 2020 RECS as sample////////////////////////////////////////////
// check racial disparity in HP adoption
cd "C:\Users\wills\Dropbox (YSE)\xingchi.shen@yale.edu's files\RECS\2020 RECS"
use "recs2020.dta",clear
keep if HOUSEHOLDER_RACE==1|HOUSEHOLDER_RACE==2
gen Hispanic=1 if SDESCENT==1
replace Hispanic=0 if Hispanic==.
gen White=1 if HOUSEHOLDER_RACE==1 & Hispanic==0
replace White=0 if White==.
gen Black=1 if HOUSEHOLDER_RACE==2 & Hispanic==0
replace Black=0 if Black==.
egen REGIONC_g=group(REGIONC)
reg HP Hispanic Black i.REGIONC_g [aw=NWEIGHT]
egen DIVISION_g=group(DIVISION)
reg HP Hispanic Black i.DIVISION_g [aw=NWEIGHT]
reg HP Hispanic Black i.STATE_FIPS [aw=NWEIGHT]
keep if inlist(state_postal, "SC", "NC", "VA", "MD", "DE", "CT", "PA", "RI", "MA")
reg HP Hispanic Black [aw=NWEIGHT]
reg HP Hispanic Black i.STATE_FIPS [aw=NWEIGHT]

// show the importance of building age
use "recs2020.dta",clear
keep if HOUSEHOLDER_RACE==1|HOUSEHOLDER_RACE==2
gen Hispanic=1 if SDESCENT==1
replace Hispanic=0 if Hispanic==.
gen White=1 if HOUSEHOLDER_RACE==1 & Hispanic==0
replace White=0 if White==.
gen Black=1 if HOUSEHOLDER_RACE==2 & Hispanic==0
replace Black=0 if Black==.
gen SF=1 if TYPEHUQ==2
replace SF=0 if SF==.
gen own=1 if KOWNRENT==1
replace own=0 if own==.
foreach i of varlist YEARMADERANGE ADQINSUL SF BEDROOMS own MONEYPY Hispanic Black{
qui sum `i' [weight=NWEIGHT]
gen sumwt=`r(sum_w)'
gen wtmean=`r(mean)'
egen double CSS=total(NWEIGHT*(`i'-wtmean)^2)
gen double variance=CSS/sumwt
gen double std_`i'=(`i'-wtmean)/sqrt(variance)
drop sumwt wtmean CSS variance
}
areg HP std_YEARMADERANGE std_SF std_BEDROOMS std_own std_MONEYPY std_Hispanic std_Black [aw=NWEIGHT], absorb(STATE_FIPS)
areg HP std_YEARMADERANGE std_ADQINSUL std_SF std_BEDROOMS std_own std_MONEYPY std_Hispanic std_Black  [aw=NWEIGHT], absorb(STATE_FIPS)
drop std_YEARMADERANGE std_ADQINSUL std_SF std_BEDROOMS std_own std_MONEYPY std_Hispanic std_Black 
save temp.dta,replace
keep if own==1
foreach i of varlist YEARMADERANGE ADQINSUL SF BEDROOMS own MONEYPY Hispanic Black {
qui sum `i' [weight=NWEIGHT]
gen sumwt=`r(sum_w)'
gen wtmean=`r(mean)'
egen double CSS=total(NWEIGHT*(`i'-wtmean)^2)
gen double variance=CSS/sumwt
gen double std_`i'=(`i'-wtmean)/sqrt(variance)
drop sumwt wtmean CSS variance
}
areg HP std_YEARMADERANGE std_SF std_BEDROOMS std_MONEYPY std_Hispanic std_Black [aw=NWEIGHT], absorb(STATE_FIPS)
use temp.dta,replace
keep if own==0
foreach i of varlist YEARMADERANGE ADQINSUL SF BEDROOMS own MONEYPY Hispanic Black {
qui sum `i' [weight=NWEIGHT]
gen sumwt=`r(sum_w)'
gen wtmean=`r(mean)'
egen double CSS=total(NWEIGHT*(`i'-wtmean)^2)
gen double variance=CSS/sumwt
gen double std_`i'=(`i'-wtmean)/sqrt(variance)
drop sumwt wtmean CSS variance
}
areg HP std_YEARMADERANGE std_SF std_BEDROOMS std_MONEYPY std_Hispanic std_Black [aw=NWEIGHT], absorb(STATE_FIPS)

// Keep 9 states only
use "recs2020.dta",clear
keep if inlist(state_postal, "SC", "NC", "VA", "MD", "DE", "CT", "PA", "RI", "MA")
keep if HOUSEHOLDER_RACE==1|HOUSEHOLDER_RACE==2
gen Hispanic=1 if SDESCENT==1
replace Hispanic=0 if Hispanic==.
gen White=1 if HOUSEHOLDER_RACE==1 & Hispanic==0
replace White=0 if White==.
gen Black=1 if HOUSEHOLDER_RACE==2 & Hispanic==0
replace Black=0 if Black==.
gen SF=1 if TYPEHUQ==2
replace SF=0 if SF==.
gen own=1 if KOWNRENT==1
replace own=0 if own==.
foreach i of varlist YEARMADERANGE ADQINSUL SF BEDROOMS own MONEYPY Hispanic Black{
qui sum `i' [weight=NWEIGHT]
gen sumwt=`r(sum_w)'
gen wtmean=`r(mean)'
egen double CSS=total(NWEIGHT*(`i'-wtmean)^2)
gen double variance=CSS/sumwt
gen double std_`i'=(`i'-wtmean)/sqrt(variance)
drop sumwt wtmean CSS variance
}
areg HP std_YEARMADERANGE std_SF std_BEDROOMS std_own std_MONEYPY std_Hispanic std_Black[aw=NWEIGHT], absorb(STATE_FIPS)
areg HP std_YEARMADERANGE std_ADQINSUL std_SF std_BEDROOMS std_own std_MONEYPY std_Hispanic std_Black [aw=NWEIGHT], absorb(STATE_FIPS)
// still consistent - building age is the most important among household features
drop std_YEARMADERANGE std_ADQINSUL std_SF std_BEDROOMS std_own std_MONEYPY std_Hispanic std_Black
save temp.dta,replace
keep if own==1
foreach i of varlist YEARMADERANGE ADQINSUL SF BEDROOMS own MONEYPY Hispanic Black{
qui sum `i' [weight=NWEIGHT]
gen sumwt=`r(sum_w)'
gen wtmean=`r(mean)'
egen double CSS=total(NWEIGHT*(`i'-wtmean)^2)
gen double variance=CSS/sumwt
gen double std_`i'=(`i'-wtmean)/sqrt(variance)
drop sumwt wtmean CSS variance
}
areg HP std_YEARMADERANGE std_SF std_BEDROOMS std_MONEYPY std_Hispanic std_Black [aw=NWEIGHT], absorb(STATE_FIPS)
use temp.dta,replace
keep if own==0
foreach i of varlist YEARMADERANGE ADQINSUL SF BEDROOMS own MONEYPY Hispanic Black{
qui sum `i' [weight=NWEIGHT]
gen sumwt=`r(sum_w)'
gen wtmean=`r(mean)'
egen double CSS=total(NWEIGHT*(`i'-wtmean)^2)
gen double variance=CSS/sumwt
gen double std_`i'=(`i'-wtmean)/sqrt(variance)
drop sumwt wtmean CSS variance
}
areg HP std_YEARMADERANGE std_SF std_BEDROOMS std_MONEYPY std_Hispanic std_Black [aw=NWEIGHT], absorb(STATE_FIPS)









// Check the relationship between income and HP adoption
// Nationwide
use "recs2020.dta",clear
gen income=1 if MONEYPY<=6 // income <=20k
replace income=2 if MONEYPY==7|MONEYPY==8 // income 20k - 30k
replace income=3 if MONEYPY==9|MONEYPY==10 // income 30k - 40k
replace income=4 if MONEYPY==11 // income 40k - 50k
replace income=5 if MONEYPY==12 // income 50k - 60k
replace income=6 if MONEYPY==13 // income 60k - 75k
replace income=7 if MONEYPY==14 // income 75k - 100k
replace income=8 if MONEYPY==15 // income 100k - 150k
replace income=9 if MONEYPY==16 // income >150k
bysort income:sum HP  [aw=NWEIGHT]

//////////////////// South Atlantic //////////////////////////////////////////////////
use "recs2020.dta",clear
keep if DIVISION=="South Atlantic"
gen income=1 if MONEYPY<=6 // income <=20k
replace income=2 if MONEYPY==7|MONEYPY==8 // income 20k - 30k
replace income=3 if MONEYPY==9|MONEYPY==10 // income 30k - 40k
replace income=4 if MONEYPY==11 // income 40k - 50k
replace income=5 if MONEYPY==12 // income 50k - 60k
replace income=6 if MONEYPY==13 // income 60k - 75k
replace income=7 if MONEYPY==14 // income 75k - 100k
replace income=8 if MONEYPY==15 // income 100k - 150k
replace income=9 if MONEYPY==16 // income >150k
bysort income:sum HP  [aw=NWEIGHT]



//////////////////// SC NC VA MD DE //////////////////////////////////////////////////
use "recs2020.dta",clear
keep if state_postal=="SC"|state_postal=="NC"|state_postal=="VA"|state_postal=="MD"|state_postal=="DE"
gen income=1 if MONEYPY<=6 // income <=20k
replace income=2 if MONEYPY==7|MONEYPY==8 // income 20k - 30k
replace income=3 if MONEYPY==9|MONEYPY==10 // income 30k - 40k
replace income=4 if MONEYPY==11 // income 40k - 50k
replace income=5 if MONEYPY==12 // income 50k - 60k
replace income=6 if MONEYPY==13 // income 60k - 75k
replace income=7 if MONEYPY==14 // income 75k - 100k
replace income=8 if MONEYPY==15 // income 100k - 150k
replace income=9 if MONEYPY==16 // income >150k
bysort income:sum HP  [aw=NWEIGHT]
















