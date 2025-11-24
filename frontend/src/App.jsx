import Wallets from './components/Wallets'

export default function App(){
  return (
    <div className="min-h-screen text-gray-900 dark:text-gray-100" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '100vh'}}>
      <header className="site-header w-full">
        <div className="container">
          <img className="site-logo" src="https://www.vaneck.com/static/corp/images/logo-blue-70.svg" alt="VanEck" />
          <div className="site-title">Crypto Wallet Checker</div>
        </div>
      </header>
      <main className="w-full max-w-4xl px-4 py-6" style={{margin: '0 auto', maxWidth: '64rem'}}>
        <Wallets />
      </main>
    </div>
  )
}
