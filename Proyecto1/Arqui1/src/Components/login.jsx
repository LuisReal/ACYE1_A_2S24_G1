

import { useNavigate } from "react-router-dom";

import birdIMG from "../assets/bird.png";
import raspberryIMG from "../assets/rapsberry.png";
import domotica1IMG from "../assets/domotica1.jpg"; // importantes hacer esto para que las imagenes sean importadas con npm run build


export default function Login() { // esto es un componente y esta disponible para ser usado en otro
  
  
  const navigate = useNavigate()
  
  //console.log("La info del id es: ", value)
  let username;
  let password;

  const validarUsuario = async(e) => {
    e.preventDefault();
    
    username = e.target.username.value
    password = e.target.password.value
    //grupo#_seccion_proy1
    if(username == "admin" & password == "123"){
        
        localStorage.setItem("auth", "true");
        navigate(`/control`)
        
    }else{
        alert("ACCESO DENEGADO");
    }
    
    
}

  return (
    <>
      
      
      <div style={{position: "relative",  marginLeft:280}}>

            <div className="sidenav">
                    
                    <h2>Sign in</h2>
                    <img className="image-bird" src={birdIMG} width="50" height="50" />
                    {/*<img className="image-logo" src={logoIMG} width="100" height="100"/> */}
                    <div class="example1">
                        <div class="reversible reversibleImagen">
                            <div id="atras">
                                <img src={raspberryIMG} />
                            </div>
                            <div id="adelante">
                                <img src={domotica1IMG} />
                            </div>
                        </div>
                    </div>
                
            </div>
            <div className="main">
                    
                    <form onSubmit={validarUsuario}>

                        <div className="banner">

                            
                        </div>

                        <div className="form-group">
                            
                            <input type="text" className="form-user" placeholder="User Name" name="username" />
                        </div>
                        <div className="form-group">
                            
                            <input type="password" className="form-password" placeholder="Password" name="password" />
                        </div>

                        <div className="botones">
                        
                            <button type="submit" className="btnL">Login</button>
                        
                        
                        </div>

                    </form>

                
            
            </div>
      
      </div>
    
     
    </>
   )
 }