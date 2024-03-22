package main

type Hs_data struct {
	HSData_Id           int     `json:"HSData_Id"`
	Lane_Id             string  `json:"Lane_Id"`
	HSData_DT           string  `json:"HSData_DT"`
	Oper_Direc          string  `json:"Oper_Direc"`
	Axle_Num            int     `json:"Axle_Num"`
	AxleGrp_Num         int     `json:"AxleGrp_Num"`
	Gross_Load          int     `json:"Gross_Load"`
	Veh_Type            int     `json:"Veh_Type"`
	AxleWt1             int     `json:"AxleWt1"`
	AxleWt2             int     `json:"AxleWt2"`
	AxleWt3             int     `json:"AxleWt3"`
	AxleWt4             int     `json:"AxleWt4"`
	AxleWt5             int     `json:"AxleWt5"`
	AxleWt6             int     `json:"AxleWt6"`
	AxleWt7             int     `json:"AxleWt7"`
	AxleWt8             int     `json:"AxleWt8"`
	AxleGrpWt1          int     `json:"AxleGrpWt1"`
	AxleGrpWt2          int     `json:"AxleGrpWt2"`
	AxleGrpWt3          int     `json:"AxleGrpWt3"`
	AxleGrpWt4          int     `json:"AxleGrpWt4"`
	AxleGrpWt5          int     `json:"AxleGrpWt5"`
	AxleGrpWt6          int     `json:"AxleGrpWt6"`
	AxleGrpWt7          int     `json:"AxleGrpWt7"`
	AxleGrpWt8          int     `json:"AxleGrpWt8"`
	AxleDis1            int     `json:"AxleDis1"`
	AxleDis2            int     `json:"AxleDis2"`
	AxleDis3            int     `json:"AxleDis3"`
	AxleDis4            int     `json:"AxleDis4"`
	AxleDis5            int     `json:"AxleDis5"`
	AxleDis6            int     `json:"AxleDis6"`
	AxleDis7            int     `json:"AxleDis7"`
	Violation_Id        int     `json:"Violation_Id"`
	OverLoad_Sign       int     `json:"OverLoad_Sign"`
	BeliefValue         int     `json:"BeliefValue"`
	Speed               int     `json:"Speed"`
	Acceleration        float64 `json:"Acceleration"`
	Temperature         int     `json:"Temperature"`
	Veh_Length          int     `json:"Veh_Length"`
	Veh_Width           int     `json:"Veh_Width"`
	Veh_Heigth          int     `json:"Veh_Heigth"`
	QAT                 float64 `json:"QAT"`
	License_Plate       string  `json:"License_Plate"`
	License_Plate_Color string  `json:"License_Plate_Color"`
	AxleSpeed1          int     `json:"AxleSpeed1"`
	AxleSpeed2          int     `json:"AxleSpeed2"`
	AxleSpeed3          int     `json:"AxleSpeed3"`
	AxleSpeed4          int     `json:"AxleSpeed4"`
	AxleSpeed5          int     `json:"AxleSpeed5"`
	AxleSpeed6          int     `json:"AxleSpeed6"`
	AxleSpeed7          int     `json:"AxleSpeed7"`
	AxleSpeed8          int     `json:"AxleSpeed8"`
	AxleGrpType1        int     `json:"AxleGrpType1"`
	AxleGrpType2        int     `json:"AxleGrpType2"`
	AxleGrpType3        int     `json:"AxleGrpType3"`
	AxleGrpType4        int     `json:"AxleGrpType4"`
	AxleGrpType5        int     `json:"AxleGrpType5"`
	AxleGrpType6        int     `json:"AxleGrpType6"`
	AxleGrpType7        int     `json:"AxleGrpType7"`
	AxleGrpType8        int     `json:"AxleGrpType8"`
	PlayStart_Time      string  `json:"PlayStart_Time"`
	PlayEnd_Time        string  `json:"PlayEnd_Time"`
	PlayChannel         int     `json:"PlayChannel"`
	Path_Video          string  `json:"Path_Video"`
	ChuCheVal           int     `json:"ChuCheVal"`
}

type FormData struct {
	IsTransaksi    string `json:"is_transaksi"`
	DeviceID       string `json:"device_id"`
	WimKode        string `json:"wim_kode"`
	KodeUppkb      string `json:"kode_uppkb"`
	TglPenimbangan string `json:"tgl_penimbangan"`
	NoKendaraan    string `json:"no_kendaraan"`
	Sumbu          int    `json:"sumbu"`
	FotoDepan      string `json:"foto_Depan"`
	FotoPlateNo    string `json:"fotoPlateNo"`
	WimBerat       int    `json:"wim_berat"`
	WimPanjang     int    `json:"wim_panjang"`
	WimLebar       int    `json:"wim_lebar"`
	WimTinggi      int    `json:"wim_tinggi"`
	WimFoh         int    `json:"wim_foh"`
	WimRoh         int    `json:"wim_roh"`
	WimKec         int    `json:"wim_kec"`
}

type Credentials struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type TokenResponse struct {
	Token string `json:"token"`
}
