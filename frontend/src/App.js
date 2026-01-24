// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
/*import React, { Component, Fragment } from "react";
import Header from "./components/Header";
import Home from "./components/Home";

class App extends Component {
  render() {
    return (
      <Fragment>
        <Header />
        <Home />
      </Fragment>
    );
  }
}

export default App;*/
//##########
// src/App.js
import React from 'react';
import AImodelsList from './components/chooseUsecase';
import ChatOldChats from './components/ChatOldChats';
import ChatDetails from './components/ChatDetails';
// import DynamicForm from './components/DynamicForm2';
import DynamicForm from './components/DynamicForm2';
// import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Chatbot from "react-chatbot-kit";
// import "react-chatbot-kit/build/main.css";

// import Chatbot from "./components/Chatbot/my"
import { useParams } from 'react-router-dom';
import ChatbotWrapper from './components/MyChat/ChatbotWrapper';
import FeedbackForm from './components/Feedback';
import Greeting from './components/course/Greeting';
import Products from './components/course/Products';
function App() {
  // const queryId = 2;
  //   return (
  //   //   <div className="App">
  //   //   <h1>My Application</h1>
  //   //   <Chatbot />
  //   // </div>
  //   //   <div className="App">
  //   //   <Chatbot config={config} messageParser={MessageParser} actionProvider={ActionProvider} />
  //   // </div>
  //   //   <Router>
  //   //   <Routes>
  //   //     <Route path="" element={<AImodelsList />} />
  //   //     <Route path="/usecase/:modelid" element={<DynamicForm />} />
  //   //   </Routes>
  //   // </Router> 
  //   // <div>
  //   //   <FeedbackForm queryId={queryId} />
  //   // </div>
  
  
  
  //     <Router>
  //   <Routes>
  //     <Route path="/" element={<AImodelsList />} />
  //     <Route path="/usecase/:modelid" element={<ChatOldChats />} />
  //     <Route path="/feedback/:queryId" element={<FeedbackForm/>}/>
  //     <Route path="/chats/:id" element={<ChatDetails />} /> {/* Ensure this route has a component */}

  //   </Routes>
  // </Router>  
  // );

  return(<Products></Products>)

}

export default App;
