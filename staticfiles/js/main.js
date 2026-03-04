
import { CountUp } from './countUp.min.js';

window.onload = function() {
  var countUpOptions = {
      useEasing: true,
      useGrouping: true,
      duration: 3,
      decimalPlaces: 0,
      separator: ",",
      decimal: ".",
  }

  $('.countUp').each(function(i, v){
    var countUp = new CountUp(v, $(v).html(), countUpOptions)
    countUp.start()
  })
  
}