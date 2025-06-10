import { Header, Footer, Form } from "../components/aio.tsx";
import { useLocation } from 'react-router-dom'
import api from '../api.js';
import "../css/aio.css"
import { useEffect, useState } from 'react'

function Home(){
const [user, setUser] = useState(null);
const location = useLocation()
const checkSession = async () => {
try {
  const result = await api.get('/auth/me');
  console.log(result)
  if (result.data.status_code !== 403) {
    setUser(result.data.user);
    console.log(result.data)
    }
    } catch (error) {
    console.log(error);
}};

  useEffect(() => {
    checkSession();
  }, [location]);

  return (
    <>
      <Header user={user} setUser={setUser} />
      {user ? null : <Form user={user} setUser={setUser}/>}
      
      <Footer/>
    </>
  )
}

export default Home