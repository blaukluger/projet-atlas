import { useEffect , useState  } from 'react'

function App() {
  const [message, setMessage] = useState('Chargement . . .')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [user, setUser] = useState(null)
  const [error, setError] = useState('')

  const [tickets, setTickets] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  
  useEffect(() => {
    if (user){
       fetch('http://localhost:8000/tickets')
       .then(res => res.json())
       .then(data => setTickets(data))
       .catch(err => console.error('Erreur chargement tickets' , err))
   }
  }, [user])

   const handlelogin = async (e) => {
    e.preventDefault()
    try{
        const rest = await fetch ('http://localhost:8000/auth/login',{
        method :'POST',
        headers : {'Content-Type': 'application/json'},
        body: JSON.stringify({email,password})
        })
        const data = await rest.json()
        if(!rest.ok) throw new Error(data.detail || 'Erreur de connection')
        setUser(data)
    } catch(err) {
      console.error(err)
      setError(err.message)
    }
  }

  // Créer un ticket
  const handleCreateTicket = async (e) => {
    e.preventDefault()
    try{
    const rest = await fetch ('http://localhost:8000/tickets',{
      method :'POST',
      headers : {'Content-Type': 'application/json'},
      body: JSON.stringify({
        title,
        description,
        category: 'Réseau',
        priority: 'Normale',
        created_by: user?.id || 1 
      })
    })
    if (rest.ok){
      alert('Ticket crée avec succès !')
      setTitle('')
      setDescription('')
        //Rechargement de la page
        window.location.reload()
      }else{
        alert('Erreur lors de la création')
        }
  }catch (err){
    console.error(err)
  }
}

 if(!user)
  return (
    <div style={{padding: '20px',fontFamily: 'Arial'}}>
    <h1>Connection - Projet Atlas</h1>
    <form onSubmit={handlelogin}>
      <input
          type='email'
          placeholder='Email'
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
          style={{marginRight: '10px', padding: '5px'}}
          />

           <input
          type='password'
          placeholder='Mot de passe'
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          style={{marginRight: '10px', padding: '5px'}}
          />
          <button type='submit' style={{padding: '5px 10px'}}>Se connecter</button>
    </form>
    {error && <p style={{olor: 'red',marginTop: '10px'}}>{error}</p>}
    </div>
  )

     


  // Si Utilisateur n'est pas connecté on affiche la page de connection
  if(user)
  return (
    <div style={{padding: '20px',fontFamily: 'Arial'}}>
      <h1>Tableau de bord - Projet Atlas</h1>
      <p>Connecter en tant que : <strong>{user.email}</strong>(Rôle: {user.role})</p>
      <button onClick={() => setUser(null)} style={{background:'#dc3545',color:'white',padding:'5px 10px', border:'none',cursor:'pointer'}}>Se déconnecter</button>
    <hr style={{margin: '20px 0'}} />
    <h3>Créer un ticket</h3>
    <form onSubmit={handleCreateTicket}>
    <input type ="text"placeholder='Titre du ticket' value={title} onChange={e => setTitle(e.target.value)}required style={{marginRight:'10px',padding : '5px'}} />
     <input type ="text"placeholder='Description' value={description} onChange={e => setDescription(e.target.value)}required style={{marginRight:'10px',padding : '5px'}} />
    <button type ='submit' style={{padding :'5px 10px'}}>Ajouter</button>
    </form>
    <h3>Liste des tickets</h3>
    <ul>
      {Array.isArray(tickets) && tickets.map(t =>(
      <li key={t.id}><strong>{t.title}</strong> Statut : {t.status} ({t.priority})</li>
      ))}
      
    </ul>
    </div>
    )
  }

export default App
