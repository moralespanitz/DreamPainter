import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from "axios";

const InputTextComponent = (props: any) => {
  const [loading, setLoading] = useState(false)
  const [sentence, setSetence] = useState("");

  function generateImage(sentence: string) {
    setLoading(true);
    axios.post(`${URL}/generate`, {
      sentence: sentence
    }).then(
      (data: any) => {
        data.forEach(
          (picture: any) => {
            props.setImage((photo: any) => [...photo, picture.key])
          }
        )
      }
    ).catch(
      error => alert(error)
    ).finally(
      () => setLoading(false)
    );
  }

  function handleChange(event: any) {
    setSetence(event.target.value);
  }

  function handleSubmit(event: any) {
    event.preventDefault()
    if (sentence === "") return alert("Ingresa una oración para ejecutar la operacion");
    alert(`The sentence is ${sentence}`)
    // generateImage(sentence);
  }


  return (
    <form onSubmit={handleSubmit} className='h-full justify-center items-center flex flex-col px-32 gap-4'>
      <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400">Imagina algo, y escríbelo aquí</label>
      <textarea id="message" rows={4} className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Escribe lo que imaginaste" onChange={handleChange}></textarea>
      {loading ?
        <button disabled type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center">
          <svg role="status" className="inline mr-3 w-4 h-4 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB" />
            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor" />
          </svg>
          Loading...
        </button>
        :
        <button
          type="submit"
          // onClick={() => { props.setSection(2) }} 
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
          Sueña
        </button>
      }
    </form >
  )
}

const GenerateImageComponent = (props: any) => {
  return (
    <div className='h-full justify-center items-center flex flex-col px-24 gap-4'>
      <div className='flex flex-row-reverse w-full'>
        <button onClick={() => { props.setSection(1) }}>
          <svg className="w-6 h-6" fill="none" stroke="currentColor" style={{ userSelect: 'auto' }} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" style={{ userSelect: "auto" }}></path></svg>
        </button>
      </div>
      <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400">Descarga tu imagen</label>
      <img className="max-w-lg h-auto rounded-lg" src="https://pbs.twimg.com/media/FbEF7X6XwAARQpI?format=png&name=small" alt="image description" />
      <div className="flex flex-row justify-evenly w-full px-10 items-center">
        <p className='w-52'>Subelo a tus redes, y escribe #OpenDayUTEC</p>
        <img className="max-w-lg h-32 rounded-lg" src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/QR_code_for_mobile_English_Wikipedia.svg/1200px-QR_code_for_mobile_English_Wikipedia.svg.png" alt="image description" />
      </div>
    </div>
  )
}
const Test = () => {
  const [urlImage, setUrlImage] = useState(-1);
  async function getImage() {
    const response = await axios({
      method: 'post',
      url: 'http://localhost:8000/generate',
      data: {
        sentence: "Hello world",
      },
    });
    setUrlImage(response.data.id);
  }
  return (
    <div>
      <button className='bg-blue-300' onClick={getImage}>
        Get image
      </button>
      <img src={
        (urlImage !== -1 ?
          `http://localhost:8000/image/${urlImage}` : "")
      } />
    </div>
  )
}
function App() {
  const [section, setSection] = useState(1);
  const [image, setImage] = useState([]);

  return (
    <div className='h-screen bg-white md:px-16 sm:px-10 lg:px-24 xl:px-32 2xl:px-64 py-10'>
      <div className='h-full bg-white rounded-lg shadow-2xl'>
        {/* {
          section == 1 ? <InputTextComponent setSection={setSection} setImage={setImage}/>
            : <GenerateImageComponent setSection={setSection} setImage={setImage}/>
        } */}
        <Test />
      </div>
    </div>
  );
}

export default App;
