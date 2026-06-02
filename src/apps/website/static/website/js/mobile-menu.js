window.addEventListener('resize', setVhUnit)

function setVhUnit(){
  const vh 				= window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`)
}
setVhUnit()

document.addEventListener('DOMContentLoaded', () => {
	const mobileMenu 	= document.getElementById('mobile_menu');
	const toggleBtn 	= document.getElementById('mobile_toggle');
	const closeBtn 		= document.getElementById('mobile_close');

	toggleBtn.addEventListener('click', (e)=>{
		e.preventDefault()
		mobileMenu.classList.add('open')
		document.body.style.overflow = 'hidden'
	})

	closeBtn.addEventListener('click', (e)=>{
		e.preventDefault()
		mobileMenu.classList.remove('open')
		document.body.style.overflow = ''
	})
})
