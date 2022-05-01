import React from 'react'

export const CryptoPrices = ({ ListOfSymbols }) => {

    return(
    <>  
        {
            ListOfSymbols.map(sym=>{
                return(
                    <table key = {sym.symbol}>
                        <tbody>
                            <tr className='gridder'>
                                <td className='gridder'>{sym.symbol}  {sym.price}</td>
                                <td className='gridder'> Checked at:{sym.checkedAt} </td>
                            </tr>

                        </tbody>
                    </table>
                )
            })
        }
    </>
    )
}