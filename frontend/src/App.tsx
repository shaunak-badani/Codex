import './App.css'
import { Card } from "@/components/ui/card"
// import { SidebarProvider } from './components/ui/sidebar'
// import Sidebar from './components/custom-sidebar'
import useGlobalStore from './store/store'
import ErrorOverlay from './model-cards/error-overlay'
import Home from './pages/Home'
import { BrowserRouter } from "react-router-dom";

function App() {
  const error = useGlobalStore(state => state.error);
  console.log("Error: ", error);

  return (
    <BrowserRouter>
    <>
    <div>
      {/* <SidebarProvider> */}
      {/* <Sidebar> */}

      <ErrorOverlay />
      
        <Card className="grid grid-cols-3 grid-gap-4">
          <div className="col-span-1" />
          <div className="header p-6 text-4xl font-extrabold lg:text-4xl">
            Codex
          </div>
        </Card>
        <div className="min-h-screen p-8 pb-8 sm:p-8">      
          <main className="max-w-4xl mx-auto flex flex-col gap-16">
            <Home />
          </main>
        </div>
    {/* </Sidebar> */}
    {/* </SidebarProvider> */}
    </div>
    
      
    </>
    </BrowserRouter>
  )
}

export default App
