package housedroid

import (
  "fmt"
  "net/http"
  "encoding/json"
  "io/ioutil"
  "bytes"
)

type Signal struct {
  id string
  data string
}

var manctrl Signal

func init() {
  http.HandleFunc("/", handler)
  http.HandleFunc("/getData", getData)
  http.HandleFunc("/sendData", sendData)
}

func handler(w http.ResponseWriter, r *http.Request) {
  html := "This is the server side for the HouseDroid project\n"
  html += "/sendData is used to send data\n"
  html += "/getData is used to get data\n"
  fmt.Fprint(w, html)
}

func sendData(w http.ResponseWriter, r *http.Request) {
  if r.Body == nil {
    return
  }
  body, _ := ioutil.ReadAll(r.Body)
  json.Unmarshal(body, &manctrl)
  fmt.Fprint(w, "send")
}

func getData(w http.ResponseWriter, r *http.Request) {
  var mybuf bytes.Buffer
  buffer.WriteString("get: ")
  buffer.WriteString(manctrl->data)
  fmt.Fprint(w, buffer.String())
}

