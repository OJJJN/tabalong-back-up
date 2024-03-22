package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/MakMoinee/go-mith/pkg/mysql"
	_ "github.com/go-sql-driver/mysql"
)

var broadcast = make(chan Hs_data) // broadcast channel
var list = []Hs_data{}             // global list of Hs_datas
var listMutex = &sync.RWMutex{}

func handleConnections(w http.ResponseWriter, r *http.Request) {
	var msg Hs_data
	// Decode the incoming request into the Hs_datas struct
	err := json.NewDecoder(r.Body).Decode(&msg)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	// Send the newly received message to the broadcast channel
	broadcast <- msg
}

func handleGetHs_data(w http.ResponseWriter, _ *http.Request) {
	listMutex.RLock()
	defer listMutex.RUnlock()

	// Create a new slice to store selected fields
	formDatas := make([]FormData, len(list))

	// Iterate over each Hs_data in the list and extract selected fields
	for i, hsData := range list {
		// Create the initial SelectedFields object
		formData := FormData{
			IsTransaksi:    "2",
			DeviceID:       "3",
			WimKode:        "WIM2",
			KodeUppkb:      "TBG",
			TglPenimbangan: hsData.HSData_DT,
			NoKendaraan:    hsData.License_Plate,
			Sumbu:          hsData.Axle_Num,
			FotoDepan:      "-",
			FotoPlateNo:    "-",
			WimBerat:       hsData.Gross_Load,
			WimPanjang:     hsData.Veh_Length,
			WimLebar:       hsData.Veh_Width,
			WimTinggi:      hsData.Veh_Heigth,
			WimFoh:         hsData.AxleDis1,
			WimRoh:         hsData.AxleDis2,
			WimKec:         hsData.Speed,
		}

		formDatas[i] = formData
	}

	// Convert the selected fields slice to JSON
	jsonList, err := json.Marshal(formDatas)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Set the content type to application/json
	w.Header().Set("Content-Type", "application/json")

	// Write the json to the response body
	w.Write(jsonList)
}

func handlePost() {
	// Step 1: Authenticate and get token
	data := Credentials{
		Email:    "wim@jto.online", // replace with your email
		Password: "wim123456",      // replace with your password
	}

	// Marshal credentials data to JSON
	payloadBytes, err := json.Marshal(data)
	if err != nil {
		log.Fatalf("Error marshalling credentials: %v", err)
	}

	// Create a request body from the JSON data
	body := bytes.NewReader(payloadBytes)

	// Create a POST request to authenticate and get token
	req, err := http.NewRequest("POST", "http://10.29.85.14:8021/api/v2pb/login", body)
	if err != nil {
		log.Fatalf("Error creating request: %v", err)
	}

	// Set request headers
	req.Header.Set("Content-Type", "application/json")

	// Send the request
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Fatalf("Error sending request: %v", err)
	}
	defer resp.Body.Close()

	// Read the response body
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading response body: %v", err)
	}

	// Unmarshal response to get the token
	var tokenResponse TokenResponse
	err = json.Unmarshal(bodyBytes, &tokenResponse)
	if err != nil {
		log.Fatalf("Error unmarshalling token response: %v", err)
	}

	token := tokenResponse.Token
	fmt.Println("Received token:", token)

	// Fetch the latest Hs_data from the list
	listMutex.RLock()
	defer listMutex.RUnlock()
	if len(list) == 0 {
		log.Println("No Hs_data available to post.")
		return
	}
	latestHsData := list[0] // Assuming the latest data is at index 0

	// Prepare form data for the POST request
	formData := map[string]string{
		"IsTransaksi":    "2",
		"DeviceID":       "3",
		"WimKode":        "WIM2",
		"KodeUppkb":      "TBG",
		"TglPenimbangan": latestHsData.HSData_DT,
		"NoKendaraan":    latestHsData.License_Plate,
		"Sumbu":          strconv.Itoa(latestHsData.Axle_Num),
		"FotoDepan":      "-", // Assuming the value is always "-"
		"FotoPlateNo":    "-", // Assuming the value is always "-"
		"WimBerat":       strconv.Itoa(latestHsData.Gross_Load),
		"WimPanjang":     strconv.Itoa(latestHsData.Veh_Length),
		"WimLebar":       strconv.Itoa(latestHsData.Veh_Width),
		"WimTinggi":      strconv.Itoa(latestHsData.Veh_Heigth),
		"WimFoh":         strconv.Itoa(latestHsData.AxleDis1),
		"WimRoh":         strconv.Itoa(latestHsData.AxleDis2),
		"WimKec":         strconv.Itoa(latestHsData.Speed),
	}

	// Encode the form data
	formDataEncoded := url.Values{}
	for key, value := range formData {
		formDataEncoded.Set(key, value)
	}

	// Create a POST request with form data
	req, err = http.NewRequest("POST", "http://10.29.85.14:8021/api/v2pv/penimbangan/create", strings.NewReader(formDataEncoded.Encode()))
	if err != nil {
		log.Fatalf("Error creating request: %v", err)
	}

	// Set request headers
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Set("Authorization", "Bearer "+token)

	// Send the request
	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		log.Fatalf("Error sending request: %v", err)
	}
	defer resp.Body.Close()

	// Read the response body
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading response body: %v", err)
	}

	// Parse the response JSON
	var response struct {
		Success bool   `json:"success"`
		Message string `json:"message"`
		Data    string `json:"data,omitempty"`
	}
	err = json.Unmarshal(respBody, &response)
	if err != nil {
		log.Fatalf("Error parsing response: %v", err)
	}

	// Handle the response based on success or failure
	if response.Success {
		fmt.Println("Response: Success")
		fmt.Println("Message:", response.Message)
		if response.Data != "" {
			fmt.Println("Data:", response.Data)
		}
	} else {
		fmt.Println("Response: Failure")
		fmt.Println("Message:", response.Message)
	}
}

func handleMessages() {
	for msg := range broadcast {
		// Log the message
		log.Printf("Received message: %+v\n", msg)
	}
}

func main() {
	flag.Parse()

	log.Println("Starting the service ....")

	// Use a WaitGroup to manage goroutines
	var wg sync.WaitGroup

	// Start handlePost goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		handlePost()
	}()

	ticker := time.NewTicker(1 * time.Second) // fires every 1 second
	defer ticker.Stop()

	// Start handleMessages goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		handleMessages()
	}()

	// Configure routes
	http.HandleFunc("/hs_data", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			handleConnections(w, r)
		} else if r.Method == http.MethodGet {
			handleGetHs_data(w, r)
		} else {
			http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		}
	})

	// Fetch initial data from MySQL
	list = fetchMysqlData()

	// Start a goroutine to fetch data from MySQL periodically
	wg.Add(1)
	go func() {
		defer wg.Done()
		for range ticker.C {
			newList := fetchMysqlData()
			listMutex.Lock()
			list = newList
			listMutex.Unlock()

			fmt.Println("Received new data from MySQL")
		}
	}()

	// Start the HTTP server
	err := http.ListenAndServe("192.168.1.125:8080", nil)
	if err != nil {
		log.Fatalf("http.ListenAndServe failed with %s\n", err)
	}

	// Wait for all goroutines to finish
	wg.Wait()
}

func fetchMysqlData() []Hs_data {
	// Define the struct
	newMysql := mysql.NewGoMithMysql("highspeednew", "localhost", "root", "wanji168", "mysql") // replace CorrectFunctionName with the correct function name
	newMysql.SetConnectionString("root:wanji168@tcp(localhost:3306)/highspeednew", 1)

	db := newMysql.GetDBConnection()
	result, err := db.Query("SELECT * FROM hs_data ORDER BY HSData_Id DESC LIMIT ?", 10)
	if err != nil {
		panic(err.Error())
	}
	defer db.Close()
	defer result.Close()

	list := []Hs_data{}

	for result.Next() {
		newHs_data := Hs_data{}
		err := result.Scan(
			&newHs_data.HSData_Id,
			&newHs_data.Lane_Id,
			&newHs_data.HSData_DT,
			&newHs_data.Oper_Direc,
			&newHs_data.Axle_Num,
			&newHs_data.AxleGrp_Num,
			&newHs_data.Gross_Load,
			&newHs_data.Veh_Type,
			&newHs_data.AxleWt1,
			&newHs_data.AxleWt2,
			&newHs_data.AxleWt3,
			&newHs_data.AxleWt4,
			&newHs_data.AxleWt5,
			&newHs_data.AxleWt6,
			&newHs_data.AxleWt7,
			&newHs_data.AxleWt8,
			&newHs_data.AxleGrpWt1,
			&newHs_data.AxleGrpWt2,
			&newHs_data.AxleGrpWt3,
			&newHs_data.AxleGrpWt4,
			&newHs_data.AxleGrpWt5,
			&newHs_data.AxleGrpWt6,
			&newHs_data.AxleGrpWt7,
			&newHs_data.AxleGrpWt8,
			&newHs_data.AxleDis1,
			&newHs_data.AxleDis2,
			&newHs_data.AxleDis3,
			&newHs_data.AxleDis4,
			&newHs_data.AxleDis5,
			&newHs_data.AxleDis6,
			&newHs_data.AxleDis7,
			&newHs_data.Violation_Id,
			&newHs_data.OverLoad_Sign,
			&newHs_data.BeliefValue,
			&newHs_data.Speed,
			&newHs_data.Acceleration,
			&newHs_data.Temperature,
			&newHs_data.Veh_Length,
			&newHs_data.Veh_Width,
			&newHs_data.Veh_Heigth,
			&newHs_data.QAT,
			&newHs_data.License_Plate,
			&newHs_data.License_Plate_Color,
			&newHs_data.AxleSpeed1,
			&newHs_data.AxleSpeed2,
			&newHs_data.AxleSpeed3,
			&newHs_data.AxleSpeed4,
			&newHs_data.AxleSpeed5,
			&newHs_data.AxleSpeed6,
			&newHs_data.AxleSpeed7,
			&newHs_data.AxleSpeed8,
			&newHs_data.AxleGrpType1,
			&newHs_data.AxleGrpType2,
			&newHs_data.AxleGrpType3,
			&newHs_data.AxleGrpType4,
			&newHs_data.AxleGrpType5,
			&newHs_data.AxleGrpType6,
			&newHs_data.AxleGrpType7,
			&newHs_data.AxleGrpType8,
			&newHs_data.PlayStart_Time,
			&newHs_data.PlayEnd_Time,
			&newHs_data.PlayChannel,
			&newHs_data.Path_Video,
			&newHs_data.ChuCheVal,
		)
		if err != nil {
			log.Printf("Error: %v", err)
			continue
		}

		list = append(list, newHs_data)

		broadcast <- newHs_data
	}

	return list
}
