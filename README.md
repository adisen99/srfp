# srfp

SRFP Summer Project

Working on Air quality forecast evaluation. Some important online sources -

Some online resources -

http://stableboundarylayer.yolasite.com/

https://duckduckgo.com/?q=boundary+layer+and+air+pollution+dispersion&t=brave&ia=web&iai=r1-19&page=2&sexp=%7B%22biaexp%22%3A%22b%22%2C%22msvrtexp%22%3A%22b%22%7D

# TODO

- [ ] Calculate the NMSE, and calc corr coeff and p-value to get significance
- [ ] For the different cities, convert the raw data from IST to UTC using the same function used for Delhi observation met_data.
- [ ] Read about Effect size and how to report it alongside p-value for a more scientifically accurate evaluation - [CHECK THIS](https://www.simplypsychology.org/effect-size.html)

## Variability against the anomaly
- [ ] Read and possibly implement low freq. and high freq. Variability.
- [ ] Plot of box-plots time-series to see Variability against the AQI anomaly for all three months
- [ ] Find the probability distribution of all data sets Check this - [DATA distribution](https://towardsdatascience.com/identify-your-datas-distribution-d76062fc0802)
- [ ] Use the distribution information to make box-plots time-series or skewness time-series and compare it against the anomaly time-series to compare the Variability of model and observation data and see at which anomaly the variability differs i.e. for high anomalies and low anomalies to see the performance of model at situations/days of high variability of AQI.
- The idea is to take 3 day average and plot the box-plots time-series
- Then compare the time-series against the variability time-series to see how the model skewness changes for days of high variability and days of low variability.

