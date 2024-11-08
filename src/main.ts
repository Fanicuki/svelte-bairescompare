import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'
import './style.css'
import './styles.css'


const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
