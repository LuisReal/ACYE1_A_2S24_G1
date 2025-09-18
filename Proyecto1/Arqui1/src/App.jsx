import React, { useState, useEffect } from "react";
import "./App.css"

import Login from "./Components/login"
import Control from "./Components/control"
import Dashboard from "./Components/dashboard"


import {
  Routes,
  Route,
  Link,
  
 } from "react-router-dom";


 function App() {

  const [sensorData, setSensorData] = useState({
    temperature: [],
    light: [],
    air:[],
    ingreso:[],
    tanque:[], //[1,0,1,0,1,0,""]
    fecha_tanque: [],
    fecha_ingreso: [],
    fecha_air: [],
    fecha_tempt: [],
    fecha_luz: [],
    //alarm: [],
    timestamps: []
  });

  

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:6789");
    // Escucha los mensajes desde el WebSocket y actualiza el estado
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        const timestamp = new Date().toLocaleTimeString();
  
        setSensorData((prevData) => ({
          temperature: [...prevData.temperature, data.temperature.temperature],
          light: [...prevData.light, data.light.light],
          air: [...prevData.air, data.air.air],
          ingreso: [...prevData.ingreso, data.ingreso.ingreso],
          tanque: [...prevData.tanque, data.tanque.tanque],
        
          fecha_tempt: [...prevData.fecha_tempt, data.temperature.fecha],
          fecha_luz: [...prevData.fecha_luz, data.light.fecha],
          fecha_air: [...prevData.fecha_air, data.air.fecha],
          fecha_ingreso: [...prevData.fecha_ingreso, data.ingreso.fecha],
          fecha_tanque: [...prevData.fecha_tanque, data.tanque.fecha],
          
          //alarm: [...prevData.alarm, data.alarm],
          timestamps: [...prevData.timestamps, timestamp]
        }));
      };
      
      return () => {
        socket.close();
      };
    
  }, []);
 


  return (
    
    <>
      
      
      <div>

        <h1 id= "sistema" style={{color:"white", textAlign:"center"}} >SMART HOME</h1>

        <div id = "navbar" className="d-flex flex-column flex-shrink-0 p-3" style={{width:280, position:"fixed", marginTop:-57,  backgroundColor:"rgb(93, 173, 226)", minHeight: "100vh"}}>
         
          <ul className="nav nav-pills flex-column mb-auto" style={{color:"white", width:250 }}>
            
            <li className="nav-item">

            <Link to="/" id="enlace" style={{color: "white", textDecoration:"none", fontSize:"20px", width:"100px"}} aria-current="page">Dashboard</Link>
            {/*<button onClick={pantalla1} id="b1" style={{width:250}} class="nav-link link-dark" aria-current="page">Pantalla1 </button>*/}
            </li>
            <hr/>
            <li>
            <Link to="/login" id="enlace" style={{color: "white", textDecoration:"none", fontSize:"20px", width:"100px"}} >Login</Link>
              {/*<button onClick={pantalla2} id="b2" style={{width:250}} class="nav-link link-dark">Pantalla2</button>*/}
            </li>
            <hr/>
            
            
          </ul>

          
        </div>

        <Routes>
          <Route path="/" element={<Dashboard sensorData={sensorData}/>}></Route>
          <Route path="/login" element={<Login/>}></Route>
          <Route path="/control" element={<Control/>}></Route>
        </Routes>
        
      </div>

     
    </>
    
  )
}

export default App
