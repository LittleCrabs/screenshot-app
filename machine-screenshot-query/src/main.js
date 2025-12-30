import { createApp } from 'vue'
import { Locale } from 'vant'
import enUS from 'vant/es/locale/lang/en-US'
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
  Tag,
  Empty,
  Progress,
} from 'vant'
import 'vant/lib/index.css'
import './style.css'
import App from './App.vue'

// 设置 Vant 为英文
Locale.use('en-US', enUS)

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
app.use(Tag)
app.use(Empty)
app.use(Progress)

app.mount('#app')
