# Synthetic data only. Base R; no package dependencies.
# Put the six CSVs in the working directory. Change cohort settings below.
as_of <- as.Date('2026-09-27'); ward <- 'PHC-S'
organism_filter <- 'Escherichia coli'; specimen_filter <- 'urine'
p <- read.csv('patients.csv'); c <- read.csv('cultures.csv'); i <- read.csv('isolates.csv'); s <- read.csv('susceptibility.csv')
x <- merge(merge(i,c,by='culture_id'),p,by='patient_id')
x$sample_date <- as.Date(x$sample_date)
x <- x[(ward=='ALL' | x$ward_code==ward) & x$organism==organism_filter & x$specimen==specimen_filter,]
report <- function(days) {
 d <- x[x$sample_date >= as_of-days+1 & x$sample_date <= as_of,]
 d <- d[order(d$sample_date,d$culture_id,d$isolate_id),]
 d <- d[!duplicated(d[c('patient_id','organism','specimen')]),]
 tests <- s[s$isolate_id %in% d$isolate_id & s$result %in% c('S','R'),]
 if (!nrow(tests)) return(NULL)
 do.call(rbind,lapply(split(tests,tests$antibiotic_code),function(z){
 n <- nrow(z); r <- sum(z$result=='R')
 data.frame(period_days=days,antibiotic=z$antibiotic_code[1],n=n,R=r,S=n-r,resistance_pct=if(n>=30)100*r/n else NA,susceptibility_pct=if(n>=30)100*(n-r)/n else NA)
 }))
}
output <- rbind(report(28),report(365))
write.csv(output,'resistance_statistics.csv',row.names=FALSE,na='')
print(output)
