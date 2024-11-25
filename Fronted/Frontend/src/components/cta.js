import React from 'react'

import PropTypes from 'prop-types'

import './cta.css'

const CTA = (props) => {
  return (
    <div className={`thq-section-padding ${props.rootClassName} `}>
      <div className="thq-section-max-width">
        <div className="cta-accent2-bg">
          <div className="cta-accent1-bg">
            <div className="cta-container2">
              <div className="cta-content">
                <span className="thq-heading-2">{props.heading1}</span>
                <p className="thq-body-large">{props.content1}</p>
              </div>
              <div className="cta-actions">
                <button type="button" className="thq-button-filled cta-button">
                  {props.action1}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

CTA.defaultProps = {
  action1: 'Get Started Now!',
  rootClassName: '',
  content1:
    'Get start now to experience the full range of services and take your website to the next level.',
  heading1: "Unlock Your Website's Potential",
}

CTA.propTypes = {
  action1: PropTypes.string,
  rootClassName: PropTypes.string,
  content1: PropTypes.string,
  heading1: PropTypes.string,
}

export default CTA
