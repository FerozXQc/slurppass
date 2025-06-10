import '../css/passlog.css'
import { useEffect, useRef } from 'react'
import api from '../api.js'
export function Passlog({task_id,title,desc,passlog,delPassLog}){

    return <div className='passlog'>
        <h3>Title: {title}</h3>
        <p>Task_id: {task_id}</p>
        <p>Desc: {desc}</p>
        <p>Password: {passlog}</p>
        <button onClick={()=>{delPassLog(task_id)}}>delete</button>
    </div>
}

export function PassForm({user, listupdate,setToggleForm}){
    const titleRef = useRef()
    const descRef = useRef()
    const passRef = useRef()

    const addPassLog = async() =>{
        const result = await api.post('/passlog/addPassLog', {user_id:user,title:titleRef.current.value,desc:descRef.current.value,passlog:passRef.current.value});
        console.log(result.data);
    }

    const passSubmit = (e) =>{
        e.preventDefault();
        addPassLog()
        listupdate()
        setToggleForm(false)

        
    }

    return <form onSubmit={passSubmit}>
        <h3>Add PassLog</h3>
        <input type="text" ref={titleRef} placeholder='title' />
        <input type="text" ref={descRef} placeholder='description'/>
        <input type="text" ref={passRef} placeholder='password'/>
        <button type='submit'>submit</button>
        
    </form>
}