
import { Line } from "react-chartjs-2";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from "chart.js";
  
  // Registrar los componentes de chart.js que vamos a utilizar
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

export default function Dashboard({ sensorData }) { // esto es un componente y esta disponible para ser usado en otro


  // Configuración de la gráfica
  const chartTemperature = {
    labels: sensorData.fecha_tempt, // ["12:00", "12:01", "12:02", "12:03", "12:04"],
    datasets: [
    {
        label: "Temperature (°C)",
        data: sensorData.temperature,
        borderColor: "rgba(254, 99, 132, 1)",
        fill: false,
        tension: 0.1
    }
    
    ]
  }

  const chartLight = {
    labels: sensorData.fecha_luz, // ["12:00", "12:01", "12:02", "12:03", "12:04"],
    datasets: [
    {
        label: "Light ",
        data: sensorData.light,//[300, 450, 500, 600, 650],
        borderColor: "rgba(54, 162, 235, 1)",
        fill: false,
        tension: 0.1
    }
    
    ]
  }

  const chartAir = {
    labels: sensorData.fecha_air, // ["12:00", "12:01", "12:02", "12:03", "12:04"],
    datasets: [
    {
        label: "Aire",
        data: sensorData.air,//[300, 450, 500, 600, 650],
        borderColor: "rgba(29, 234, 91, 1)", //29, 234, 91
        fill: false,
        tension: 0.1
    }
    
    ]
  }

  const chartIngreso = {
    labels: sensorData.fecha_ingreso, // ["12:00", "12:01", "12:02", "12:03", "12:04"],
    datasets: [
    {
        label: "Ingreso Casa",
        data: sensorData.ingreso,//[300, 450, 500, 600, 650],
        borderColor: "rgba(218, 238, 18, 1)", //218, 238, 18 
        fill: false,
        tension: 0.1
    }
    
    ]
  }


  const chartTanque = {
    labels: sensorData.fecha_tanque,
    datasets: [
    {
        label: "Tanque de Agua",
        data: sensorData.tanque,
        borderColor: "rgba(161, 18, 238, 1)", //161, 18, 238
        fill: false,
        tension: 0.1
    }
    
    ]
  }

  const options = {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Sensor Data',
        }
      }
  }

  return (
    <div>
      <h1 style={{marginLeft:"300px",borderBottomColor:"green", borderBottomStyle:"solid", fontSize:"30px", width:"300px"}}>GRAFICAS</h1>
      <div style={{marginLeft:"300px", width: "1200px", height: "800px" }}>
        <Line data={chartTemperature} options={options}/>
      </div>
      <div style={{marginLeft:"300px", width: "1200px", height: "800px" }}>
        <Line data={chartLight} options={options}/>
      </div>
      
      <div style={{marginLeft:"300px", width: "1200px", height: "800px" }}>
        <Line data={chartAir} options={options}/>
      </div>
      <div style={{marginLeft:"300px", width: "1200px", height: "800px" }}>
        <Line data={chartIngreso} options={options}/>
      </div>

      <div style={{ marginLeft: "300px", width: "1200px", height: "800px" }}>
        <Line data={chartTanque} options={options} />
      </div>
      
      <h1 style={{marginLeft:"300px",borderBottomColor:"green", borderBottomStyle:"solid", fontSize:"30px", width:"600px"}}>TABLA DE VALORES DE LOS SENSORES</h1>
      
      <div style={{ marginLeft: "300px", marginTop:"50px", display: "flex" }}>
        <div>
          <table border='1' style={{marginLeft:"50px",borderCollapse: "collapse" }}>
          
            
          
            <thead>
              <tr><th colSpan="3" style={{textAlign:"center"}}>Sensor Temperatura</th></tr>
              <tr><th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Cantidad</th>
                <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Temperatura</th>
                <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Fecha</th></tr>
            </thead>
            
            <tbody>
              {sensorData.temperature.map((temp, index) => 
              temp !== "" ?(
                  <tr key={index}>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{index}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{temp}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{sensorData.fecha_tempt[index]}</td>
                  </tr>
                ):null)}
            </tbody>
          </table>
        </div>
        

        <div>
          <table border='1' style={{marginLeft:"50px",borderCollapse: "collapse" }}>
            
            <thead>
              <tr><th colSpan="3" style={{textAlign:"center"}}>Sensor Luz</th></tr>
              <tr><th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Cantidad</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Luz</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Fecha</th></tr>
            </thead>
            
            <tbody>
              {sensorData.light.map((luz, index) => 
              luz !== "" ?(
                  <tr key={index}>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{index}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{luz}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{sensorData.fecha_luz[index]}</td>
                  </tr>
                ):null)}
            </tbody>
          </table>
        </div>
        
          
        <div>
          <table border='1' style={{marginLeft:"50px",borderCollapse: "collapse" }}>
            
            <thead>
              <tr><th colSpan="3" style={{textAlign:"center"}}>Aire Acondicionado</th></tr>
              <tr><th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Cantidad</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Aire</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Fecha</th></tr>
            </thead>
            
            <tbody>
              {sensorData.air.map((aire, index) => 
              aire !== "" ?(
                  <tr key={index}>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{index}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{aire}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{sensorData.fecha_air[index]}</td>
                  </tr>
                ):null)}
            </tbody>
          </table>

          </div>
        
        <div>
          <table border='1' style={{marginLeft:"50px",borderCollapse: "collapse", tableLayout: "fixed", overflowY: "auto" }}>
            
            <thead>
              <tr><th colSpan="3" style={{textAlign:"center"}}>Acceso Casa</th></tr>
              <tr><th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Cantidad</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Ingreso</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Fecha</th></tr>
            </thead>
            
            <tbody>
              {sensorData.ingreso.map((access, index) => 
              access !== "" ? (
                  <tr key={index}>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{index}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{access}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{sensorData.fecha_ingreso[index]}</td>
                  </tr>
                ):null)}
            </tbody>
          </table>

        </div>
        
        <div>
          <table border='1' style={{marginLeft:"50px",borderCollapse: "collapse", tableLayout: "fixed" }}>
            
            <thead>
              <tr><th colSpan="3" style={{textAlign:"center"}}>Tanque de agua</th></tr>
              <tr><th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Cantidad</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Tanque</th>
              <th style={{border:"1px solid", padding:"8px", textAlign:"center"}}>Fecha</th></tr>
            </thead>
            
            <tbody>
              {sensorData.tanque.map((tanque, index) => 
              tanque !== "" ? (
                  <tr key={index}>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{index}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{tanque}</td>
                    <td style={{border:"1px solid", padding:"8px", textAlign:"center"}}>{sensorData.fecha_tanque[index]}</td>
                  </tr>
                ):null)}
            </tbody>
          </table>
        </div>
        

      </div>
      
      

    </div>
  )
}