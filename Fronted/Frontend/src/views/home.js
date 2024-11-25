import React from 'react'

import { Helmet } from 'react-helmet'
import Hero from '../components/hero'
import Steps1 from '../components/steps1'
import CTA from '../components/cta'
import Features21 from '../components/features21'
import Team8 from '../components/team8'
import Testimonial from '../components/testimonial'
import Pricing from '../components/pricing'
import Contact from '../components/contact'
import Footer from '../components/footer'
import './home.css'

const Home = (props) => {
  return (
    <div className="home-container">
      <Helmet>
        <title>WebAnalyzer</title>
      </Helmet>
      <Hero rootClassName="heroroot-class-name"></Hero>
      <Steps1></Steps1>
      <CTA rootClassName="ct-aroot-class-name"></CTA>
      <Features21></Features21>
      <Team8></Team8>
      <Testimonial></Testimonial>
      <Pricing></Pricing>
      <Contact></Contact>
      <Footer></Footer>
    </div>
  )
}

export default Home
