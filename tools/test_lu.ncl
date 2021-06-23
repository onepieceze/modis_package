;   Example script plots all data in a geo_em file
;   November 2008

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

begin
  a = addfile("/THFS/home/iap-ys/model/WRFV3/test/run20120623_modis_mp16_cu1_speta50_minlevel34/wrfout_d03_2012-06-24_00:00:00.nc","r")   ; Open a file
 ; v = a->LU_INDEX        ; Read the variable to memory
  v = wrf_user_getvar(a,"LU_INDEX",-1)
  type = "x11"
; type = "pdf"
; printMinMax(v, True)
  wks = gsn_open_wks(type,"LU_modis_d3")    
 ; f = 1
 ; atan_f = atan(f);返回的单位是弧度！！
 ;  a = tan(1) 
 ; r2d = 45.0/atan(1.0) 
 ; print(a)  
 ; exit

    ; lat = 23.     ;广东省 广州市 广州市经度：113.27  纬度：23.13
    ; lon = 113.50    ;广东省 深圳市 深圳市经度：114.05  纬度：22.55
                     ;广东省 中山市 中山市经度：113.38 纬度：22.52
                     ;广东省 东莞市 东莞市经度：113.75 纬度：23.05
   ;  llres = True
   ;  llres@ReturnInt = True   ; Return integer values
   ;  locij = wrf_user_ll_to_ij(a, lon, lat, llres)
   ;  locij = locij - 1        ; array pointers in NCL space
   ;  locX = locij(0)
   ;  locY = locij(1)
   ;  print(locij)        ;从中间分


    x_start = 414
    x_end   = 563
    y_start = 254
    y_end   = 399
  
  mpres = True                             ; Set map options
  mpres@mpGeophysicalLineColor = "Black"
  mpres@mpGeophysicalLineThicknessF = 2.
  mpres@mpOutlineBoundarySets = "National"
  mpres@mpNationalLineColor    = "Black"
  mpres@mpNationalLineThicknessF = 2
  mpres@mpDataSetName          = "Earth..4"
  mpres@mpDataBaseVersion      = "MediumRes" ; or "Ncarg4_1"
  mpres@mpAreaMaskingOn        = True
  mpres@mpMaskAreaSpecifiers   = (/"China"/)
  mpres@mpOutlineSpecifiers    = (/"China","China:Provinces"/)
  mpres@mpGeophysicalLineColor = "Black"
  mpres@mpNationalLineColor    = "Black"
  mpres@mpUSStateLineColor     = "Black"
  mpres@mpGridLineColor        = "Black"
  mpres@mpLimbLineColor        = "Black"
  mpres@mpPerimLineColor       = "Black"

   ;  x_start = 208
   ;  x_end   = 707
   ;  y_start = 167
   ;  y_end   = 519

    mpres@ZoomIn = True
    mpres@Xstart = x_start
    mpres@Ystart = y_start
    mpres@Xend = x_end
    mpres@Yend = y_end
  ; printVarSummary(v)
  ; exit 
  ;  v = v(0,y_start:y_end,x_start:x_end)
  ;print(a)
  v=where(v.gt.17.or.v.lt.13, 15, v)       ;这个where命令叼叼的~
  gsn_define_colormap(wks,"StepSeq25")
  
   v_0 = v(:,y_start:y_end,x_start:x_end)


  opts = True                               ; Set some Basic Plot options
  opts@InitTime = False                     ; Do not plot time or footers
  opts@Footer = False
  opts@cnFillOn = True
  
 ; opts@cnFillPattern      = 5  
  
  opts@cnFillMode           = "CellFill"
  opts@cnLevelSelectionMode = "ExplicitLevels"
  opts@cnLevels             = (/13.5,16.5/)
  opts@cnFillColors         = (/2,13,21/)     ;2红色，13绿色，21蓝色
  opts@lbLabelStrings = (/ "Urban and Built-Up Land", "Other","Water Bodies" /)

 ; opts@mpOutlineSpecifiers = (/"China:states","Taiwan"/)
 ; opts@mpOutlineBoundarySets = "NoBoundaries"
  ;opts@mpAreaMaskingOn = True
 ; opts@mpMaskAreaSpecifiers = (/"China","Taiwan","Disputed area between India and China",\
 ; "India:Arunachal Pradesh"/)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  opts@cnExplicitLabelBarLabelsOn = True
  opts@lbLabelAngleF = 270.0
  opts@lbLabelAlignment = "BoxCenters"
  opts@lbTitleOn = False
  opts@lbLabelFontHeightF = 0.01
  opts@lbLabelJust = "CenterLeft"
  opts@pmLabelBarOrthogonalPosF = 0.01
  opts@FieldTitle = "LU_INDEX : "+ v@description   ; overwrite field name

  contour = wrf_contour(a,wks,v_0(0,:,:),opts)
  plot = wrf_map_overlays(a,wks,(/contour/),True,mpres)

  print("You are a handsome boy !!")

end
