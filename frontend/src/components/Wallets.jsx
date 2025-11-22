import React, { useEffect, useState, useRef } from 'react'
import api from '../api'

export default function Wallets(){
  const [wallets, setWallets] = useState([])
  const [err, setErr] = useState(null)
  const [editingId, setEditingId] = useState(null)
  const [editingQty, setEditingQty] = useState('')
  const [editingQtyError, setEditingQtyError] = useState('')
  const [adding, setAdding] = useState(false)
  const [newAddress, setNewAddress] = useState('')
  const [newCurrency, setNewCurrency] = useState('')
  const [newQuantity, setNewQuantity] = useState('')
  const [newAddressError, setNewAddressError] = useState('')
  const [newCurrencyError, setNewCurrencyError] = useState('')
  const [newQuantityError, setNewQuantityError] = useState('')
  const [banner, setBanner] = useState(null)
  const bannerTimer = useRef(null)
  const closeTimer = useRef(null)
  const [bannerClosing, setBannerClosing] = useState(false)

  const startCloseBanner = (delay = 300) => {
    // animate then remove
    if (closeTimer.current) clearTimeout(closeTimer.current)
    setBannerClosing(true)
    closeTimer.current = setTimeout(() => {
      setBanner(null)
      setBannerClosing(false)
      closeTimer.current = null
    }, delay)
  }

  const showBanner = (b, timeout = 4000) => {
    // errors stay until manually dismissed
    if (bannerTimer.current) {
      clearTimeout(bannerTimer.current)
      bannerTimer.current = null
    }
    if (closeTimer.current) {
      clearTimeout(closeTimer.current)
      closeTimer.current = null
      setBannerClosing(false)
    }

    setBanner(b)

    if (b?.type !== 'error') {
      // auto-dismiss non-error banners
      bannerTimer.current = setTimeout(() => {
        bannerTimer.current = null
        startCloseBanner(300)
      }, timeout)
    }
  }

  const fetchWallets = async () => {
    try {
      const res = await api.get('/wallets')
      setWallets(Array.isArray(res.data) ? res.data : [])
      setErr(null)
    } catch (e) {
      setErr(String(e))
    }
  }

  useEffect(() => { fetchWallets() }, [])

  useEffect(() => {
    return () => {
      if (bannerTimer.current) {
        clearTimeout(bannerTimer.current)
        bannerTimer.current = null
      }
      if (closeTimer.current) {
        clearTimeout(closeTimer.current)
        closeTimer.current = null
      }
    }
  }, [])

  const handleRefresh = () => fetchWallets()

  const handleAdd = () => {
    setAdding(true)
    setNewAddress('')
    setNewCurrency('')
    setNewQuantity('')
  }

  const validateAdd = () => {
    let ok = true
    setNewAddressError('')
    setNewCurrencyError('')
    setNewQuantityError('')

    if(!newAddress || newAddress.trim().length === 0){
      setNewAddressError('Address is required')
      ok = false
    }
    if(!newCurrency || newCurrency.trim().length === 0){
      setNewCurrencyError('Currency is required')
      ok = false
    }
    const expected_quantity = Number(newQuantity)
    if(newQuantity === '' || Number.isNaN(expected_quantity)){
      setNewQuantityError('Quantity must be a number')
      ok = false
    } else if(expected_quantity < 0){
      setNewQuantityError('Quantity must be >= 0')
      ok = false
    }
    return ok
  }

  const submitAdd = async () => {
    if(!validateAdd()) return
    const expected_quantity = Number(newQuantity)
    try{
      await api.post('/wallets/', { address: newAddress, currency: newCurrency, expected_quantity })
      setAdding(false)
      fetchWallets()
      showBanner({ type: 'success', text: 'Wallet added' })
    }catch(e){
      showBanner({ type: 'error', text: e.response?.data?.detail || e.toString() })
    }
  }

  const cancelAdd = () => {
    setAdding(false)
    setNewAddress('')
    setNewCurrency('')
    setNewQuantity('')
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this wallet?')) return
    try {
      await api.delete(`/wallets/${id}`)
      setWallets((prev) => prev.filter((w) => w.id !== id))
      showBanner({ type: 'success', text: 'Wallet deleted' })
    } catch (e) {
      showBanner({ type: 'error', text: e.response?.data?.detail || String(e) })
    }
  }

  const startEdit = (w) => {
    setEditingId(w.id)
    setEditingQty(String(w.expected_quantity))
  }

  const cancelEdit = () => {
    setEditingId(null)
    setEditingQty('')
    setEditingQtyError('')
  }

  const saveEdit = async (id) => {
    setEditingQtyError('')
    const expected_quantity = Number(editingQty)
    if(editingQty === '' || Number.isNaN(expected_quantity)){
      setEditingQtyError('Quantity must be a number')
      return
    }
    if(expected_quantity < 0){
      setEditingQtyError('Quantity must be >= 0')
      return
    }
    try{
      await api.put(`/wallets/${id}`, { expected_quantity })
      // Update local state
      setWallets(wallets.map(w => w.id === id ? { ...w, expected_quantity } : w))
      cancelEdit()
      showBanner({ type: 'success', text: 'Wallet updated' })
    }catch(e){
      showBanner({ type: 'error', text: e.response?.data?.detail || e.toString() })
    }
  }

  

  return (
    <section className="max-w-4xl mx-auto p-4">
      {(err || banner) && (
        <div className={`${banner?.type === 'success' ? 'banner-success' : 'banner-error'} border px-4 py-2 rounded mb-4 flex items-center justify-between ${bannerClosing ? 'banner-fade-out' : 'banner-fade-in'}`}> 
          <span className="text-sm">{banner?.text || String(err)}</span>
          <button className="ml-4 text-sm" onClick={() => { if (bannerTimer.current) { clearTimeout(bannerTimer.current); bannerTimer.current = null } startCloseBanner(300); setErr(null); }}>✕</button>
        </div>
      )}

      <div className="border rounded overflow-hidden mb-4">
        <div className="flex items-center justify-between border-b px-4 h-12 table-header">
          <h2 className="text-sm font-medium m-0 h-8 flex items-center leading-none">Wallets</h2>
          <div className="flex items-center gap-2">
            <button onClick={handleRefresh} className="h-8 px-3 rounded btn btn-ghost border">Refresh</button>
            <button onClick={handleAdd} className="h-8 px-3 rounded btn btn-primary">Add Wallet</button>
          </div>
        </div>

        {adding && (
          <div className="flex flex-row flex-wrap items-center gap-3 p-4 border-b">
          <div className="flex-1 min-w-[220px]">
            <input className="border rounded px-2 h-8 w-full" placeholder="Address" value={newAddress} onChange={e => setNewAddress(e.target.value)} />
            {newAddressError && <div className="text-red-600 text-sm mt-1">{newAddressError}</div>}
          </div>
          <div className="w-28">
            <input className="border rounded px-2 h-8 w-full" placeholder="Currency" value={newCurrency} onChange={e => setNewCurrency(e.target.value)} />
            {newCurrencyError && <div className="text-red-600 text-sm mt-1">{newCurrencyError}</div>}
          </div>
          <div className="w-40">
            <input className="border rounded px-2 h-8 w-full" placeholder="Quantity" type="number" value={newQuantity} onChange={e => setNewQuantity(e.target.value)} />
            {newQuantityError && <div className="text-red-600 text-sm mt-1">{newQuantityError}</div>}
          </div>
          <div className="flex items-center gap-2">
            <button onClick={submitAdd} className="px-3 h-8 btn btn-success">Save</button>
            <button onClick={cancelAdd} className="px-3 h-8 btn btn-ghost border">Cancel</button>
          </div>
        </div>
        )}

        <div className="overflow-x-auto border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <table className="min-w-full table-auto">
            <thead>
                <tr className="bg-gray-50 dark:bg-gray-900">
                  <th className="px-4 py-3 text-left align-middle">Address</th>
                  <th className="px-4 py-3 text-left align-middle">Currency</th>
                  <th className="px-4 py-3 text-left align-middle">Quantity</th>
                  <th className="px-4 py-3 text-left align-middle">Actions</th>
                </tr>
            </thead>
            <tbody>
              {wallets.length === 0 ? (
                <tr className="border-b border-gray-200 dark:border-gray-700"><td colSpan={4} className="px-4 py-6">No wallets found</td></tr>
              ) : (
                wallets.map(w => (
                  <tr key={w.id} className="border-b border-gray-200 dark:border-gray-700 odd:bg-white even:bg-gray-50 table-row-hover">
                    <td className="px-4 py-3 font-mono">{w.address}</td>
                    <td className="px-4 py-3">{w.currency}</td>
                    <td className="px-4 py-3">
                      {editingId === w.id ? (
                        <div className="flex flex-col">
                          <input className="border rounded px-2 py-1 w-32" type="number" value={editingQty} onChange={e => setEditingQty(e.target.value)} />
                          {editingQtyError && <div className="text-red-600 text-sm mt-1">{editingQtyError}</div>}
                        </div>
                      ) : (
                        w.expected_quantity
                      )}
                    </td>
                    <td className="px-4 py-3">
                      {editingId === w.id ? (
                        <div className="flex items-center gap-2">
                          <button onClick={() => saveEdit(w.id)} className="px-2 py-1 btn btn-success">Save</button>
                          <button onClick={cancelEdit} className="px-2 py-1 btn btn-ghost border">Cancel</button>
                        </div>
                      ) : (
                        <div className="flex items-center gap-2">
                          <button onClick={() => startEdit(w)} className="px-2 py-1 btn btn-ghost border">Edit</button>
                          <button onClick={() => handleDelete(w.id)} className="px-2 py-1 btn btn-danger border">Delete</button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  )
}
