import React from 'react'

import PropTypes from 'prop-types'

import './testimonial.css'

const Testimonial = (props) => {
  return (
    <div className="thq-section-padding">
      <div className="testimonial-max-width thq-section-max-width">
        <div className="testimonial-container10">
          <h2 className="thq-heading-2">{props.heading1}</h2>
          <span className="testimonial-text11 thq-body-small">
            {props.content1}
          </span>
        </div>
        <div className="thq-grid-2">
          <div className="thq-animated-card-bg-2">
            <div className="thq-animated-card-bg-1">
              <div data-animated="true" className="thq-card testimonial-card1">
                <div className="testimonial-container12">
                  <img
                    alt={props.author1Alt}
                    src="https://play.teleporthq.io/static/svg/default-img.svg"
                    className="testimonial-image1"
                  />
                  <div className="testimonial-container13">
                    <strong className="thq-body-large">
                      {props.author1Name}
                    </strong>
                    <span className="thq-body-small">
                      {props.author1Position}
                    </span>
                  </div>
                </div>
                <span className="testimonial-text14 thq-body-small">
                  {props.review1}
                </span>
              </div>
            </div>
          </div>
          <div className="thq-animated-card-bg-2">
            <div className="thq-animated-card-bg-1">
              <div data-animated="true" className="thq-card testimonial-card2">
                <div className="testimonial-container14">
                  <img
                    alt={props.author2Alt}
                    src="https://play.teleporthq.io/static/svg/default-img.svg"
                    className="testimonial-image2"
                  />
                  <div className="testimonial-container15">
                    <strong className="thq-body-large">
                      {props.author2Name}
                    </strong>
                    <span className="thq-body-small">
                      {props.author2Position}
                    </span>
                  </div>
                </div>
                <span className="testimonial-text17 thq-body-small">
                  {props.review2}
                </span>
              </div>
            </div>
          </div>
          <div className="thq-animated-card-bg-2">
            <div className="thq-animated-card-bg-1">
              <div data-animated="true" className="thq-card testimonial-card3">
                <div className="testimonial-container16">
                  <img
                    alt={props.author3Alt}
                    src="https://play.teleporthq.io/static/svg/default-img.svg"
                    className="testimonial-image3"
                  />
                  <div className="testimonial-container17">
                    <strong className="thq-body-large">
                      {props.author3Name}
                    </strong>
                    <span className="thq-body-small">
                      {props.author3Position}
                    </span>
                  </div>
                </div>
                <span className="testimonial-text20 thq-body-small">
                  {props.review3}
                </span>
              </div>
            </div>
          </div>
          <div className="thq-animated-card-bg-2">
            <div className="thq-animated-card-bg-1">
              <div data-animated="true" className="thq-card testimonial-card4">
                <div className="testimonial-container18">
                  <img
                    alt={props.author4Alt}
                    src="https://play.teleporthq.io/static/svg/default-img.svg"
                    className="testimonial-image4"
                  />
                  <div className="testimonial-container19">
                    <strong className="thq-body-large">
                      {props.author4Name}
                    </strong>
                    <span className="thq-body-small">
                      {props.author4Position}
                    </span>
                  </div>
                </div>
                <span className="testimonial-text23 thq-body-small">
                  {props.review4}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

Testimonial.defaultProps = {
  author2Alt: 'Jane Smith Image Alt Text',
  heading1: 'Testimonials',
  author4Name: 'Sarah Lee',
  review2:
    'The UX design services provided by this platform have transformed our website into a user-friendly and visually appealing platform. Our bounce rate has decreased, and our customers are more satisfied than ever.',
  author2Name: 'Jane Smith',
  author3Position: 'CTO of Company Z',
  author1Name: 'John Doe',
  author4Position: 'SEO Specialist at Company A',
  review3:
    "With the security solutions offered by this platform, we have been able to protect our website from cyber threats and ensure the safety of our users' data. The peace of mind is invaluable.",
  author1Alt: 'John Doe Image Alt Text',
  author4Alt: 'Sarah Lee Image Alt Text',
  content1:
    "Thanks to the website optimization services, our site's performance has improved significantly. We saw a noticeable increase in user engagement and conversions.",
  author3Alt: 'David Johnson Image Alt Text',
  author2Position: 'Marketing Manager at Company Y',
  author3Name: 'David Johnson',
  review1:
    'I highly recommend this platform for anyone looking to enhance their online presence.',
  review4:
    "The SEO strategies implemented by this platform have significantly boosted our website's visibility and organic traffic. Our search engine rankings have improved, leading to a substantial increase in leads and sales.",
  author1Position: 'CEO of Company X',
}

Testimonial.propTypes = {
  author2Alt: PropTypes.string,
  heading1: PropTypes.string,
  author4Name: PropTypes.string,
  review2: PropTypes.string,
  author2Name: PropTypes.string,
  author3Position: PropTypes.string,
  author1Name: PropTypes.string,
  author4Position: PropTypes.string,
  review3: PropTypes.string,
  author1Alt: PropTypes.string,
  author4Alt: PropTypes.string,
  content1: PropTypes.string,
  author3Alt: PropTypes.string,
  author2Position: PropTypes.string,
  author3Name: PropTypes.string,
  review1: PropTypes.string,
  review4: PropTypes.string,
  author1Position: PropTypes.string,
}

export default Testimonial
