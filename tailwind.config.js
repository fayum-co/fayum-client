/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./layouts/**/*.{html,js}"],
  theme: {
    extend: {
      borderWidth:{
        1:"1px"
      } , 
      colors:{
        dark:"#171717" , 
        cream:"#F8F6EB",
        green:"#2B403A",
        light:"#FAFAFA"
        
      }
    },
  },
  plugins: [],
}