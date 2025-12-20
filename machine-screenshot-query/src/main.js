import { createApp } from 'vue'
import {
  Button,
  Field,
  Form,
  CellGroup,
  Cell,
  NavBar,
  Icon,
  Picker,
  Popup,
  Image as VanImage,
  ImagePreview,
  Toast,
  Dialog,
  Radio,
  RadioGroup,
} from 'vant'
import 'vant/lib/index.css'
import './style.css'
import App from './App.vue'

const app = createApp(App)

// 注册 Vant 组件
app.use(Button)
app.use(Field)
app.use(Form)
app.use(CellGroup)
app.use(Cell)
app.use(NavBar)
app.use(Icon)
app.use(Picker)
app.use(Popup)
app.use(VanImage)
app.use(ImagePreview)
app.use(Toast)
app.use(Dialog)
app.use(Radio)
app.use(RadioGroup)

app.mount('#app')
