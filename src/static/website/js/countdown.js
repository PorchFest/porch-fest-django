const countDownDate = new Date(2026, 3, 25, 10, 0, 0).getTime()
let x = setInterval(()=>{
  const now         = new Date().getTime()
  const distance    = countDownDate - now
  const days        = Math.floor(distance / (1000 * 60 * 60 * 24))
  const hours       = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes     = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
  const seconds     = Math.floor((distance % (1000 * 60)) / 1000)
  document.getElementById("days").innerHTML       = days
  document.getElementById("hours").innerHTML      = hours
  document.getElementById("minutes").innerHTML    = minutes
  document.getElementById("seconds").innerHTML    = seconds
  if(distance < 0){
    clearInterval(x)
    document.getElementById("counter").innerHTML  = "Porchfest!"
  }
}, 1000)