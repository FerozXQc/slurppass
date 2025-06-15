import { Header, Footer, Form } from "../components/aio.tsx";
import { useLocation } from 'react-router-dom'
import {Passlog, PassForm} from "../components/Passlog.tsx";
import api from '../api.js';
import "../css/aio.css"
import { useEffect, useState } from 'react'

function Home(){
const [user, setUser] = useState(null);
const location = useLocation()
const [logs,setLogs] = useState([{}])
const [toggleForm, setToggleForm] = useState(false)

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
    setUser(null)

}};

const listPasslogs = async()=>{
  try {
    const result = await api.get('/passlog/listPassLogs', {
      params: {
        user_id: user // This will create a URL like /passlog/listPassLogs?user_id=some_user_id
      }
    });
    setLogs(result.data) 
  } catch (error) {
    console.error("Error fetching pass logs:", error);
    setLogs([]);

  }
};

const delPasslog = async(key)=>{
  try {
    await api.delete('/passlog/deletePassLog',{
      params: {
        user_id:user,
        task_id:key
      }
    })
    listPasslogs()

  } catch (error) {
    console.error(error)
  }
}


  useEffect(() => {
    checkSession();
  }, [location]);

  useEffect(()=>{
    if(user){
    listPasslogs();
    }
    else{
      setLogs([])
    }
  },[user])

  return (
    <>
      <Header user={user} setUser={setUser} />
      {user ? null : <Form user={user} setUser={setUser}/>}
      {user ? <button onClick={()=>{setToggleForm(true)}}>add PassLog</button>: null}
      {toggleForm? <PassForm user={user} listupdate={listPasslogs} setToggleForm={setToggleForm}/> : null}
      {user ? (
  logs.length === 0 ? (
    <p>No passLogs found.</p>
  ) : (<>
    <ul>
      {logs
        .filter(loggy => loggy !== null) // <--- Add this filter!
        .map(loggy => (
        <li key={loggy.task_id}><Passlog
            task_id={loggy.task_id}
            title={loggy.title}
            desc={loggy.desc}
            passlog={loggy.passlog}
            delPassLog={delPasslog}
          /></li>
        ))}
    </ul></>
  )
) : (
  null
)}
      <Footer/>
    </>
  )
}

export default Home