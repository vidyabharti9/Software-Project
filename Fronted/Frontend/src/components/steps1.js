import React from 'react'

import PropTypes from 'prop-types'

import './steps1.css'

const Steps1 = (props) => {
  return (
    <div className="steps1-container1 thq-section-padding">
      <div className="steps1-max-width thq-section-max-width">
        <div className="steps1-container2">
          <div className="steps1-container3 thq-card">
            <h2 className="thq-heading-2">{props.step1Title}</h2>
            <span className="steps1-text2 thq-body-small">
              {props.step1Description}
            </span>
          </div>
          <div className="steps1-container4 thq-card">
            <h2 className="steps1-text3 thq-heading-2">{props.step2Title}</h2>
            <span className="steps1-text4 thq-body-small">
              {props.step2Description}
            </span>
          </div>
        </div>
        <div className="steps1-container5">
          <div className="steps1-container6 thq-card">
            <h2 className="thq-heading-2">{props.step3Title}</h2>
            <span className="steps1-text6 thq-body-small">
              {props.step3Description}
            </span>
          </div>
          <div className="steps1-container7 thq-card">
            <h2 className="thq-heading-2">{props.step4Title}</h2>
            <span className="steps1-text8 thq-body-small">
              {props.step4Description}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

Steps1.defaultProps = {
  step1Description: 'Enhance your website performance with our services',
  step4Title: 'Stay Updated',
  step1Title: 'Choose Your Plan',
  step3Title: 'See Results',
  step3Description:
    'Experience increased user engagement, enhanced security, and improved search engine visibility.',
  text: '04',
  step2Title: 'Enhance Your Website',
  step4Description:
    'Subscribe to receive the latest updates and tips to keep your website at its best.',
  step2Description:
    'Enhance website performance with our design, security, SEO strategies, and optimization services.',
}

Steps1.propTypes = {
  step1Description: PropTypes.string,
  step4Title: PropTypes.string,
  step1Title: PropTypes.string,
  step3Title: PropTypes.string,
  step3Description: PropTypes.string,
  text: PropTypes.string,
  step2Title: PropTypes.string,
  step4Description: PropTypes.string,
  step2Description: PropTypes.string,
}

export default Steps1
