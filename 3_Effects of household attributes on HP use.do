cd "C:\Users\wills\Dropbox (YSE)\xingchi.shen@yale.edu’s files\heating equity"

// the importance of building age in HP adoption

// OLS Outcome-HP - by adding different fixed effects
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
gen owner=1 if ((PROPERTYINDICATORCODE==10)|(PROPERTYINDICATORCODE==11))&(OWNER_RENTER_STATUS==9)
replace owner=0 if owner==.
summarize owner
generate s_owner = (owner - r(mean)) / r(sd)
areg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_owner s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach, absorb(ZIP)
outreg2 using results, word replace
//eststo reg1
reg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_owner s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach
outreg2 using results, word append
//eststo reg2
reg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_owner s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach i.state_group
outreg2 using results, word append
//eststo reg3
areg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_owner s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach, absorb( FIPS_CODE )
outreg2 using results, word append
//eststo reg4
//global varlist_std s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_OWNER_RENTER_STATUS s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach
//esttab reg1 reg2 reg3 reg4 using "data/Analysis/ols_estimates_HP_determinants.tex", mtitles("(1)" "(2)" "(3)" "(4)") keep($varlist_std _cons) star(* 0.10 ** 0.05 *** 0.01) collabels(none) label stats(r2 N, fmt(%9.4f %9.0fc) labels("R-squared" "Number of observations")) plain b(%9.4f) se(%9.4f) noabbrev se nonumbers lines parentheses replace fragment
// Owners only
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
keep if ((PROPERTYINDICATORCODE==10)|(PROPERTYINDICATORCODE==11))&(OWNER_RENTER_STATUS==9)
areg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach, absorb(ZIP)
outreg2 using results, word replace
reg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach
outreg2 using results, word append
reg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach i.state_group
outreg2 using results, word append
areg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach, absorb( FIPS_CODE )
outreg2 using results, word append
//Renters only
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
drop if ((PROPERTYINDICATORCODE==10)|(PROPERTYINDICATORCODE==11))&(OWNER_RENTER_STATUS==9)
areg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach, absorb(ZIP)
outreg2 using results, word replace
reg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach
outreg2 using results, word append
reg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach i.state_group
outreg2 using results, word append
areg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_Ethnic1 s_Ethnic2 s_HTDD s_elec_price s_ng_price s_Ratio_AboveBach, absorb( FIPS_CODE )
outreg2 using results, word append


// OLS Outcome-HP, within ZIP code variation
areg HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_OWNER_RENTER_STATUS s_Ethnic1 s_Ethnic2, absorb(ZIP) vce(cluster ZIP)

// coef. sensitivity test
regsensitivity HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_OWNER_RENTER_STATUS s_Ethnic1 s_Ethnic2 i.ZIP, compare(s_LIVING_AREA s_SF s_FIND_DIV_1000 s_OWNER_RENTER_STATUS s_Ethnic1 s_Ethnic2)
regsensitivity bounds HP s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_OWNER_RENTER_STATUS s_Ethnic1 s_Ethnic2 i.ZIP, compare(s_LIVING_AREA s_SF s_FIND_DIV_1000 s_OWNER_RENTER_STATUS s_Ethnic1 s_Ethnic2) cbar(0(.2)1) rxbar(0(.2)1) plot

// Decompose R2
reg HP i.ZIP
predict residuals,residuals
reg residuals s_YEARBUILT s_LIVING_AREA s_SF s_FIND_DIV_1000 s_OWNER_RENTER_STATUS s_Ethnic1 s_Ethnic2
shapley2, stat(r2)


// Nonlinear relationship between building age and HP adoption
// Warm
//Mean HP share for each decade of year built
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
keep if inlist(STATE, "SC", "NC") & YEARBUILT >= 1900 & YEARBUILT <= 2020
egen decade = cut(YEARBUILT), at(1900(10)2020) label
drop if decade==.
collapse (mean) HP, by(decade)
// regress HP on decade indicators controlling everything; plot the coef.
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
keep if inlist(STATE, "SC", "NC") & YEARBUILT >= 1900 & YEARBUILT <= 2020
drop if missing(HP, LIVING_AREA, SF, FIND_DIV_1000, OWNER_RENTER_STATUS, Ethnic1, Ethnic2, ZIP, YEARBUILT)
gen decade = floor((YEARBUILT-1900)/10)*10 + 1900
drop if decade==2020
tabulate decade, generate(decade_dummies)
drop decade_dummies1
areg HP decade_dummies* LIVING_AREA SF FIND_DIV_1000 OWNER_RENTER_STATUS, absorb(ZIP) vce(cluster ZIP)

// Temp
//Mean HP share for each decade of year built
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
keep if inlist(STATE, "VA", "MD","DE") & YEARBUILT >= 1900 & YEARBUILT <= 2020
egen decade = cut(YEARBUILT), at(1900(10)2020) label
drop if decade==.
collapse (mean) HP, by(decade)
// regress HP on decade indicators controlling everything; plot the coef.
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
keep if inlist(STATE, "VA", "MD","DE") & YEARBUILT >= 1900 & YEARBUILT <= 2020
drop if missing(HP, LIVING_AREA, SF, FIND_DIV_1000, OWNER_RENTER_STATUS, Ethnic1, Ethnic2, ZIP, YEARBUILT)
gen decade = floor((YEARBUILT-1900)/10)*10 + 1900
drop if decade==2020
tabulate decade, generate(decade_dummies)
drop decade_dummies1
areg HP decade_dummies* LIVING_AREA SF FIND_DIV_1000 OWNER_RENTER_STATUS, absorb(ZIP) vce(cluster ZIP)

// Cold
//Mean HP share for each decade of year built
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
keep if inlist(STATE, "PA", "CT", "RI", "MA") & YEARBUILT >= 1900 & YEARBUILT <= 2020
egen decade = cut(YEARBUILT), at(1900(10)2020) label
drop if decade==.
collapse (mean) HP, by(decade)
// regress HP on decade indicators controlling everything; plot the coef.
use "data\Analysis\households_9ST2021_heat_building_demographics_3races.dta",clear
keep if inlist(STATE, "PA", "CT", "RI", "MA") & YEARBUILT >= 1900 & YEARBUILT <= 2020
drop if missing(HP, LIVING_AREA, SF, FIND_DIV_1000, OWNER_RENTER_STATUS, Ethnic1, Ethnic2, ZIP, YEARBUILT)
gen decade = floor((YEARBUILT-1900)/10)*10 + 1900
drop if decade==2020
tabulate decade, generate(decade_dummies)
drop decade_dummies1
areg HP decade_dummies* LIVING_AREA SF FIND_DIV_1000 OWNER_RENTER_STATUS, absorb(ZIP) vce(cluster ZIP)






