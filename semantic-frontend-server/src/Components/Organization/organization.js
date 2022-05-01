import React from 'react'

export const Organization = ({ ListOfOrgs }) => {

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
                                <td className='gridder'>{org.cui}</td>
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