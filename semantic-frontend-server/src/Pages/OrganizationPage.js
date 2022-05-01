import React, {useState, useEffect} from 'react';
import Axios from 'axios'
import { Organization } from '../Components/Organization/organization';
import { CryptoPrices } from '../Components/Organization/bonus';

export const OrganizationPage = () => {
    const [org, setOrg] = useState([])
    const [org2, setOrg2] = useState([])
    const [org3, setOrg3] = useState([])
    const [firstname, setFname] = useState('')
    const [lastname, setLname] = useState('')
    const [age, setAge] = useState('')
    const [organizationName, setOname] = useState('')
    const [sysmessage, setSysMsg] = useState('')

    const [data, setData] = useState([])
    const [crypto, setCrypto] = useState([])

    const datetime = () => {
        return Date().toLocaleString()
    }

    const handleAddCrypto = (d) => {
        d['checkedAt'] = datetime()
        setCrypto((prevCrypto) => [
            ...prevCrypto,
            d
        ])
    }

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

    function sendDataToS2(payload){
        
        Axios.post('/postToGraphql', payload).then((response) => {
            console.log(response)
            if (response.status === 200)
            {
                setSysMsg(response.data['message'])
                Axios.get('/getOrgWEmployeesS2').then((response)=>{
                    if (response.status === 200)
                    {
                        setOrg2(response.data)
                    }
                    else {console.log(response)}
                    });
            }
 
        }).catch(function (error) {
            setSysMsg('Error occurred: ' + error.data);
          });
    }

    function sendDataToS3(payload){
        
        Axios.post('/postToRdf4j', payload).then((response) => {
            console.log(response)
            if (response.status === 200)
            {
                setSysMsg(response.data['message'])
                Axios.get('/getOrgWEmployeesS3').then((response)=>{
                    if (response.status === 200)
                    {
                        setOrg3(response.data)
                    }
                    else {console.log(response)}
                    });
            }
 
        }).catch(function (error) {
            setSysMsg('Error occurred: ' + error.data);
          });
    }

    function getCryptoPrice(symbol){
        Axios.get('https://api.binance.com/api/v3/ticker/price?symbol='+symbol).then((response) => {
            console.log(response)
            if (response.status === 200)
            {
                handleAddCrypto(response.data)
                let d = response.data
                d['checkedAt'] = datetime()
                Axios.post('/addCryptoData', d).then((r)=>{
                    console.log(r)
                }).catch(function (error) {
                    setSysMsg('Error occurred: ' + error.response.data);
                  });
            }
 
        }).catch(function (error) {
            setSysMsg('Error occurred: ' + error.data);
          });
    }

    function buildCryptoData(){

        getCryptoPrice('BTCBUSD')
        getCryptoPrice('SOLBUSD')
        getCryptoPrice('ETHBUSD')
        getCryptoPrice('MANABUSD')
        getCryptoPrice('EGLDBUSD')
        getCryptoPrice('DOGEBUSD') 

    }

    const handleBonusPoint = (e) => {
        e.preventDefault()
        setCrypto([])
        buildCryptoData()
    }

    const handles1tos2 = (e) => {
        e.preventDefault()

        sendDataToS2(data)
    }

    const handles2tos3 = (e) => {
        e.preventDefault()

        sendDataToS3(org2)
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
        <button onClick={handles1tos2}>Send to S2</button>
        <h2>Server 2 data</h2>
        <Organization ListOfOrgs={org2}/>
        <button onClick={handles2tos3}>Send to S3</button>
        <h2>Server 3 data</h2>
        <Organization ListOfOrgs={org3}/>
        <button onClick={handleBonusPoint}>Bonus point</button>
        <CryptoPrices ListOfSymbols={crypto}/>
        </>
    )
}