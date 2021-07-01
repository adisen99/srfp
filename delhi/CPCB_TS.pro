;--------------------------------------------------------------------------------------------------------
;Caluclation of Delhi mean Houraly Averegae----
;Author: Sachin D.Ghde, IITM Pune
;---------------------------------------------------------------------------------------------------------

filea ='/iitm5/wifex/chinmay/delhi_fcst/CPCB_data/PMDATA/DELHI/CPCB_data.txt'
outfile='CPCB_data_2020.out'
openw,11,outfile
  ASTR=READ_ASCII(filea)
  A=ASTR.(0)

    yy= reform(A[0,*])
    mo= reform(A[1,*])
    dd= reform(A[2,*])
    hh= reform(A[3,*])
    dp2=reform(A[5,*])
    dpm1=reform(A[4,*])

	for y=2020, 2021 do begin
        for m=01, 12 do begin
        for d=01, 31 do begin
        for h=00, 23 do begin
	
        ij = where(yy eq y and mo eq m and dd eq d and hh eq h and dp2 gt 10. and dp2 lt 1500., count)
	PM25 = mean(dp2(ij))
	PM = STDDEV(dp2(ij))

        kk = where(yy eq y and mo eq m and dd eq d and hh eq h and dpm1 gt 10. and dpm1 lt 1500., count)
        PM10 = mean(dpm1(kk))
        PMM = STDDEV(dpm1(kk))

        ll = where(yy eq y and mo eq m and dd eq d and hh eq h and dp2 le 0.0, count)
        if count eq 43 then begin 
        PM25 = !Values.F_NAN     
        endif  

        lo = where(yy eq y and mo eq m and dd eq d and hh eq h and dpm1 le 0.0, count)
        if count eq 43 then begin
        PM10 = !Values.F_NAN
        endif

        if count gt 0. then begin
	print, y,m,d,h,PM25, PM10
	printf,11,y,m,d,h,PM25,PM,PM10,PMM, format='(4A8,4F12.2)'
	endif
        endfor
        endfor
        endfor
        endfor
close,11
;spawn, 'sed -i -e 1,63d CPCB_data_2020.out'

Spawn, 'cat CPCB_data_2019.out CPCB_data_2020.out > CPCB_data.out'
spawn, 'sed -i -e 1,9001d CPCB_data.out'
;--------------------------------------------------------------------------------------------------------- 
; calculation of Running mean times series ----------
;---------------------------------------------------------------------------------------------------------
fileb = 'CPCB_data.out'
  rows=file_lines(fileb)
  BSTR=READ_ASCII(fileb)
  B=BSTR.(0)

    yy= reform(B[0,*])
    mo= reform(B[1,*])
    dd= reform(B[2,*])
    hh= reform(B[3,*])
    p2=reform(B[4,*])
    pm1=reform(B[6,*])

ind = where(FINITE(p2, /NaN))
if ind[0] gt -1 then p2[ind] = 70.

indd = where(FINITE(pm1, /NaN))
if indd[0] gt -1 then pm1[ind] = 80.

RTP2 =  TS_SMOOTH(p2,24,/BACKWARD)
RTPM1 = TS_SMOOTH(pm1,24,/BACKWARD)

print, rows
help, RTP2
;stop
outfile='CPCB_Running_Mean.out'
openw,12,outfile

for i = 23, rows-1 do begin
         print, yy[i],mo[i],dd[i],hh[i],RTP2[i], RTPM1[i]
        printf,12,FIX(yy[i]),FIX(mo[i]),FIX(dd[i]),FIX(hh[i]),RTP2[i],RTPM1[i], format='(4A8,2F12.2)'
endfor
close,12

;----------------------------------------------------------------------------------------------------------------------
;Calculation of AQI for PM2.5 and PM10
;----------------------------------------------------------------------------------------------------------------------

file='CPCB_Running_Mean.out'
rows=file_lines(file)
CSTR=READ_ASCII(file)
  C=CSTR.(0)

    yy= reform(C[0,*])
    mo= reform(C[1,*])
    dd= reform(C[2,*])
    hh= reform(C[3,*])
    p2=reform(C[4,*])
    pm1=reform(C[5,*])

Ip2 = fltarr(rows)
Ipm1 = fltarr(rows)

for i=0, rows-1 do begin

;---------------------------------------------------CPCB PM25 AQI----------------------------------
if p2[i] gt 0. and p2[i] le 30. then begin
Ip2[i] = (1.66*(p2[i]-0.))+0.
endif

if p2[i] gt 30. and p2[i] le 60. then begin
Ip2[i] = (1.66*(p2[i]-30.))+50.
endif

if p2[i] gt 60. and p2[i] le 90. then begin
Ip2[i] = (3.33*(p2[i]-60.))+100.
endif

if p2[i] gt 90. and p2[i] le 120. then begin
Ip2[i] = (3.33*(p2[i]-90.))+200.
endif

if p2[i] gt 120. and p2[i] le 250. then begin
Ip2[i] = (0.769*(p2[i]-120.))+300.
endif

if p2[i] gt 250. then begin
Ip2[i] = (0.769*(p2[i]-250.))+400.
endif
;-------------------------------------------------------------------------------------------------------------
;------------------------------------------------CPCB PM10 AQI--------------------------------------------------

if pm1[i] gt 0. and pm1[i] le 50. then begin
Ipm1[i] = (pm1[i]-0.)+0.
endif

if pm1[i] gt 50. and pm1[i] le 100. then begin
Ipm1[i] = (pm1[i]-50.)+50.
endif

if pm1[i] ge 100. and pm1[i] le 250. then begin
Ipm1[i] = (0.66*(pm1[i]-100.))+100.
endif

if pm1[i] ge 250. and pm1[i] le 350. then begin
Ipm1[i] = (pm1[i]-250.)+200.
endif

if pm1[i] ge 350. and pm1[i] le 430. then begin
Ipm1[i] = (1.25*(pm1[i]-350.))+300.
endif

if pm1[i] ge 430. then begin
Ipm1[i] = (1.25*(pm1[i]-430.))+400.
endif

endfor
;---------------------------------------------------------------------------------------------------------------------
;---------------------------------------------------Writing modeled AQI Time Series---------------------------------------------
outfile='CPCB_AQI.out'
openw,13,outfile

for j=0, rows-1 do begin

                AQI =0.0
                if Ip2[j] gt Ipm1[j] then begin
                AQI = Ip2[j]
                endif else begin
                AQI=Ipm1[j]
               endelse
        print, yy[j],mo[j],dd[j],hh[j],Ip2[j],Ipm1[j],AQI
        printf,13,FIX(yy[j]),FIX(mo[j]),FIX(dd[j]),FIX(hh[j]),FIX(Ip2[j]),FIX(Ipm1[j]), FIX(AQI), format='(7A8)'
endfor
close,13

AQI =0.0
if Ip2[rows-1] gt Ipm1[rows-1] then begin
AQI = Ip2[rows-1]
endif else begin
AQI=Ipm1[rows-1]
endelse
;------------------------------------------------------------------------------------------------------------------------
;--------------------------------------Writing current AQI file---------------------------------------------------
outfile='current_AQI.out'
openw,14,outfile
print, AQI
printf,14,FIX(yy[rows-1]),FIX(mo[rows-1]),FIX(dd[rows-1]),FIX(hh[rows-1]),FIX(AQI), format='(5A8)'
close,14

;---------------------------------------------------------------------------------------------------------------------------
;-----------------------------------Clculating daily mean---------------------------------------------------------------------

filed = 'CPCB_data.out'
  rows=file_lines(filed)
  DSTR=READ_ASCII(filed)
  D=DSTR.(0)

    yy= reform(D[0,*])
    mo= reform(D[1,*])
    dd= reform(D[2,*])
    dp2=reform(D[4,*])
    dpm1=reform(D[6,*])


        outfile='CPCB_Daily_Mean.out'
        openw,15,outfile

        for y=2019, 2021 do begin
        for m=01, 12 do begin
        for d=01, 31 do begin

        ij = where(yy eq y and mo eq m and dd eq d, count)
        PM25 = mean(dp2(ij), /NaN)
        PM = STDDEV(dp2(ij), /NaN)

        kk = where(yy eq y and mo eq m and dd eq d, count)
        PM10 = mean(dpm1(kk), /NaN)
        PMM = STDDEV(dpm1(kk), /NaN)

        if count gt 0. then begin
        print, y,m,d,PM25, PM10
        printf,15,y,m,d,PM25,PM,PM10,PMM, format='(3A8,4F12.2)'
        endif
        endfor
        endfor
        endfor

end














