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

    const data = [
        {
        oname : "",
        id : "",
        cui : "",
        employees : [
        ]
    }
    ]

    function buildData(ListOfOrgs){
        ListOfOrgs.map(org=>{
            data.push(org)
        })
        console.log(data)
    }

    function addEmployeeToData(e){
        data.forEach( (itm) => {
            if (itm.id === e.organizationId){
                console.log("workssss")
            }
        })
        console.log(data)
    }

    const handleSubmit = (e) => {
        e.preventDefault() //prevent page from refresh after clicking submit

        const sendEmployee = {firstname, lastname, age, organizationName}
        Axios.post('/addEmp', sendEmployee).then((response) => {
            setSysMsg('Employee was added successfully')
            addEmployeeToData(response.data)
            
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
                buildData(response.data)
            }
            else {console.log(response)}
            });
    },[])

    useEffect(()=>{
        Axios.get('/getOrgWEmployeesS2').then((response)=>{
            if (response.status === 200)
            {
                setOrg2(response.data)
                console.log(org2)
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