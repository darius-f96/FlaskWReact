import React, { useState, useEffect }  from 'react'

export const Organization = ({ ListOfOrgs }) => {

    const data = [
        oname = "",
        id = "",
        cui = "",
        employees = [
            firstname = "",
            lastname = "",
            age = "",
            organizationId = id
        ]
    ]

    function buildData(){
        ListOfOrgs.map(org=>{
            data.push(org)
        })
    }

    function addEmployeeToData(e){
        for (let i; i < data.length ; i++){
            if (data[i] == e.organizationId){
                data[i]['employees'].push(e)
            }
        }
    }

    return(
    <>
        {
            ListOfOrgs.map(org=>{
                return(
                    <table key = {org.id}>
                        <tbody>
                            <tr className='gridder'>
                                <td className='gridder'>{org.name}</td>
                                <td className='gridder'>{org.id}</td>
                            </tr>
                            {org.Employees?.map((emp)=> {
                                return(
                                    <tr key = {emp.id} className='gridder'>
                                        <td></td>
                                        <td className='gridder'>{emp.firstname}  {emp.lastname}</td>
                                        <td className='gridder'>{emp.age}</td>
                                    </tr>
                                )
                            })
                            
                            }
                            {org.employees?.map((emp)=> {
                                return(
                                    <tr key = {emp.id} className='gridder'>
                                        <td></td>
                                        <td className='gridder'>{emp.firstname}  {emp.lastname}</td>
                                        <td className='gridder'>{emp.age}</td>
                                    </tr>
                                )
                            })
                            
                            }
                        </tbody>
                    </table>
                )
            })
        }
    </>
    )
}