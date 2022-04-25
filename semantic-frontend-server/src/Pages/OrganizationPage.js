import React, {useState, useEffect} from 'react';
import Axios from 'axios'
import { Organization } from '../Components/Organization/organization';

export const OrganizationPage = () => {
    const [org, setOrg] = useState([])
    const [org2, setOrg2] = useState([])
    const [firstname, setFname] = useState('')
    const [lastname, setLname] = useState('')
    const [age, setAge] = useState('')
    const [organizationName, setOname] = useState('')
    const [sysmessage, setSysMsg] = useState('')

    const [data, setData] = useState([])

    function buildData(ListOfOrgs){
        let dataResult = []
        
        ListOfOrgs.forEach(item => {
            dataResult.push(item)
        })
        return dataResult
    }

    function addEmployeeToData(e){
        console.log(data)
        let dataResult = data
        dataResult.forEach(itm => {
            if (itm.id === e.organizationId){
                itm.employees.push(e)
                console.log("founddd")
                }
        
        }
        )
        return dataResult
    }

    const handleSubmit = (e) => {
        e.preventDefault() 

        const sendEmployee = {firstname, lastname, age, organizationName}
        Axios.post('/addEmp', sendEmployee).then((response) => {
            setSysMsg('Employee was added successfully')
            setData(addEmployeeToData(response.data))
            setOrg(data)
            
        }).catch(function (error) {
            setSysMsg('Error occurred: ' + error.response.data);
          });

    }

    useEffect(()=>{
        Axios.get('/getOrgWEmployees').then((response)=>{
            if (response.status === 200)
            {
                setOrg(response.data)
                console.log(response.data)
                setData(buildData(response.data))
            }
            else {console.log(response)}
            });
    },[])

    useEffect(()=>{
        Axios.get('/getOrgWEmployeesS2').then((response)=>{
            if (response.status === 200)
            {
                setOrg2(response.data)
            }
            else {console.log(response)}
            });
    },[])

    return(
        <>
        <h2>New employee</h2>
        <form onSubmit = {handleSubmit}>
            <label>First Name:</label>
            <input type ="text" required value={firstname} onChange={(i) => setFname(i.target.value)} ></input>
            <label>Last Name:</label>
            <input type ="text" required value={lastname} onChange={(i) => setLname(i.target.value)} ></input>
            <label>Age:</label>
            <input type ="number" value={age} onChange={(i) => setAge(i.target.value)} ></input>
            <label>Organization Name:</label>
            <input type ="text" required value={organizationName} onChange={(i) => setOname(i.target.value)} ></input>
            <button>Add employee</button>
        </form>
        <p>{sysmessage}</p>
        <h2>Server 1 data</h2>
        <Organization ListOfOrgs={org}/>

        <h2>Server 2 data</h2>
        <Organization ListOfOrgs={org2}/>

        </>
    )
}