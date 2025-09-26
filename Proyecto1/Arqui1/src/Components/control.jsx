import { useNavigate } from "react-router-dom";
import  { useEffect } from "react";

export default function Control() {  // esto es un componente y esta disponible para ser usado en otro
  
    const navigate = useNavigate()

    useEffect(() => {
    const auth = localStorage.getItem("auth");
    if (auth !== "true") {
      navigate("/login"); 
    }
  }, [navigate]);

  const encenderLuces = async(e) => {
    e.preventDefault();
    alert("Luces Encendidas")

    
  }

    const apagarLuces = async(e) => {
    e.preventDefault();

    alert("Luces apagadas")
    
}

const encenderAlarma = async(e) => {
    e.preventDefault();

    alert("Luces apagadas")

}

const apagarAlarma = async(e) => {
    e.preventDefault();

    alert("Luces apagadas")

}

const encenderAire = async(e) => {
    e.preventDefault();

    alert("Aire encendido")

}

const apagarAire = async(e) => {
    e.preventDefault();

    alert("aire apagado")

}

const encenderTanque = async(e) => {
    e.preventDefault();

    alert("Tanque de agua encendido")

}

const apagarTanque = async(e) => {
    e.preventDefault();

    alert("Tanque de agua apagado")

}

const logout = async(e) => {
    e.preventDefault();

    alert("cerrando sesion")
    localStorage.removeItem("auth");

    // Redirigir al login
    navigate(`/login`);

}

  return (
    <>
      
      
      <div className="contenedor" >

            <div>
              <button onClick={logout}  id="btn-logout"  className="btn btn-danger" aria-current="page">Logout </button>
            </div>

            <div className="luces">
                
                <h1 style={{borderBottomColor:"green", borderBottomStyle:"solid", fontSize:"30px", width:"300px"}}>Iluminacion</h1>
                <div className="botonesIluminacion">
                
                    <button type="submit" className="btn btn-success" onClick={encenderLuces}>Encender</button>
                    <button type="submit" className="btn btn-danger" style={{marginLeft:"50px"}} onClick={apagarLuces}>Apagar</button>
                
                </div>

            
            </div>

            <div className="alarma">
                
                <h1 style={{borderBottomColor:"green", borderBottomStyle:"solid", fontSize:"30px", width:"300px"}}>Alarma Incendio</h1>
                <div className="botonesAlarma">
                
                    <button type="submit" className="btn btn-success" onClick={encenderAlarma}>Encender</button>
                    <button type="submit" className="btn btn-danger" style={{marginLeft:"50px"}} onClick={apagarAlarma}>Apagar</button>
                
                </div>

            
            </div>

            <div className="aire">
                
                <h1 style={{borderBottomColor:"green", borderBottomStyle:"solid", fontSize:"30px", width:"300px"}}>Aire Acondicionado</h1>
                <div className="botonesAire">
                
                    <button type="submit" className="btn btn-success" onClick={encenderAire}>Encender</button>
                    <button type="submit" className="btn btn-danger" style={{marginLeft:"50px"}} onClick={apagarAire}>Apagar</button>
                
                </div>

            
            </div>

            <div className="tanque">
                
                <h1 style={{borderBottomColor:"green", borderBottomStyle:"solid", fontSize:"30px", width:"300px"}}>Tanque de Agua</h1>
                <div className="botonesTanque">
                
                    <button type="submit" className="btn btn-success" onClick={encenderTanque}>Encender</button>
                    <button type="submit" className="btn btn-danger" style={{marginLeft:"50px"}} onClick={apagarTanque}>Apagar</button>
                
                </div>

            
            </div>
      
      </div>
    
     
    </>
   )
 }