import React from 'react'

import { Helmet } from 'react-helmet'

import Stats8 from '../components/stats8'
import FAQ11 from '../components/faq11'
import Footer1 from '../components/footer1'
import './learn.css'

const Learn = (props) => {
  return (
    <div className="learn-container">
      <Helmet>
        <title>Learn - Spotless Hungry Crocodile</title>
        <meta property="og:title" content="Learn - Spotless Hungry Crocodile" />
      </Helmet>

      <Stats8 heading1="Importance of this feature"></Stats8>
      <FAQ11></FAQ11>
      <Footer1></Footer1>
    </div>
  )
}

export default Learn
