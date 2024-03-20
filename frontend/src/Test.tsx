import { FormEvent } from 'react'
import './App.css'

async function send(event: FormEvent<HTMLFormElement>) {
  event.preventDefault()
  const formDate = new FormData(event.currentTarget)
  const name = formDate.get('name')
  const desc = formDate.get('description')
  const P = formDate.get('price')
  const T = formDate.get('tax')
  console.error(`you give me this : '${name}' && '${desc}' && '${P}' && '${T}'`)
  const myHeaders = new Headers();
  myHeaders.append("accept", "application/json");
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
  });

  const requestOptions = {
    method: "GET",
    headers: myHeaders,
    body: raw,
  };

  fetch("http://localhost:8000/data", requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}

function App() {

  return (
    <>
      <form onSubmit={send}>
        <label>
          Name:
          <input type="text" name="name" />
        </label>
        <label>
          Description:
          <input type="text" name="description" />
        </label>
        <label>
          price:
          <input type="text" name="price" />
        </label>
        <label>
          tax:
          <input type="text" name="tax" />
        </label>
        <button type='submit'>send</button>
      </form>
    </>
  )
}

export default App