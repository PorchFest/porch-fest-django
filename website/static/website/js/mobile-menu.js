window.addEventListener('resize', setVhUnit)

function setVhUnit(){
  const vh 				= window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`)
}
setVhUnit()

document.addEventListener('DOMContentLoaded', ()=>{
	const mobileMenu 	= document.getElementById('mobile_menu')
	const page 			= document.getElementById('page')
	let showMenu 		= false
	document.getElementById('mobile_toggle').addEventListener('click', ()=>{
		displayToggle(mobileMenu)
	})
	mobileMenu.addEventListener('click', ()=>{
		displayToggle(mobileMenu)
	})
	mobileMenu.addEventListener('transitionend', ()=>{
		removeTransition(mobileMenu)
	})
	function displayToggle(el){
		if(!showMenu){
			document.body.style.overflow = 'hidden';
			el.classList.add('transition')
			el.clientWidth
			el.classList.remove('hidden')
			showMenu 	= true
		}else{
			document.body.style.overflow = '';
			el.classList.add('transition')
			el.classList.add('hidden')
			showMenu 	= false
		}
	}
	function removeTransition(el){
		el.classList.remove('transition')
	}
})