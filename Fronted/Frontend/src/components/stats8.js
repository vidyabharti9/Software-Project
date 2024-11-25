import React from 'react'

import PropTypes from 'prop-types'

import Toast61 from './toast61'
import './stats8.css'

const Stats8 = (props) => {
  return (
    <div id="slider" className="slider thq-section-padding">
      <Toast61 rootClassName="toast61root-class-name"></Toast61>
      <div className="stats8-max-width1 thq-section-max-width">
        <div className="stats8-container2">
          <h2 className="thq-heading-2 stats8-title">{props.heading1}</h2>
        </div>
        <div className="stats8-container3 thq-grid-4">
          <div className="stats8-container4 thq-card thq-box-shadow">
            <h2 className="thq-heading-2">{props.stat1}</h2>
            <span className="thq-body-small">
              {props.stat1ShortDescription}
            </span>
            <p className="stats8-text12 thq-body-large">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
          </div>
          <div className="stats8-container5 thq-card thq-box-shadow">
            <h2 className="thq-heading-2">{props.stat2}</h2>
            <span className="thq-body-small">
              {props.stat2ShortDescription}
            </span>
            <p className="stats8-text15 thq-body-large">
              {props.stat2Description}
            </p>
          </div>
          <div className="stats8-container6 thq-card thq-box-shadow">
            <h2 className="thq-heading-2">{props.stat3}</h2>
            <span className="thq-body-small">
              {props.stat3ShortDescription}
            </span>
            <p className="stats8-text18 thq-body-large">
              {props.stat3Description}
            </p>
          </div>
          <div className="stats8-container7 thq-card thq-box-shadow">
            <h2 className="thq-heading-2">{props.stat4}</h2>
            <span className="thq-body-small">
              {props.stat4ShortDescription}
            </span>
            <p className="stats8-text21 thq-body-large">
              {props.stat4Description}
            </p>
          </div>
        </div>
      </div>
      <div className="stats8-max-width2 thq-section-max-width">
        <div className="thq-card thq-flex-column">
          <h1 className="thq-heading-1 stats8-text22">
            Learn the parameters used by us.
          </h1>
          <div className="thq-divider-horizontal"></div>
          <span className="stats8-text23 thq-body-small">
            Discover how our services can boost your website performance and
            drive results.
          </span>
          <button type="button" className="stats8-button thq-button-flat">
            <span className="thq-body-small">Read more</span>
            <svg viewBox="0 0 1024 1024" className="thq-icon-small">
              <path d="M426 256l256 256-256 256-60-60 196-196-196-196z"></path>
            </svg>
          </button>
          <div className="stats8-content8">
            <div className="stats8-author"></div>
          </div>
        </div>
        <ul className="stats8-ul list thq-flex-column">
          <li className="list-item thq-flex-column">
            <h2 className="stats8-heading1 thq-heading-2">
              UI Design Services
            </h2>
            <p className="thq-body-small">
              Our team of experienced designers focuses on creating visually
              appealing and user-friendly interfaces to enhance the overall user
              experience of your website.
            </p>
          </li>
          <li className="list-item">
            <h3 className="thq-heading-3">Security Solutions</h3>
            <p className="thq-body-small">
              We offer robust security solutions to protect your website from
              cyber threats and ensure the safety of your data and your
              visitors&apos; information.
            </p>
          </li>
          <li className="list-item">
            <h3 className="thq-heading-3">SEO Strategies</h3>
            <p className="thq-body-small">
              Our SEO experts work to improve your website&apos;s search engine
              rankings, drive organic traffic, and increase visibility on the
              web.
            </p>
          </li>
          <li className="list-item">
            <h3 className="thq-heading-3">Online Advertising Credits</h3>
            <p className="thq-body-small">
              Get access to online advertising credits to promote your website
              and reach a wider audience through various digital marketing
              channels.
            </p>
          </li>
          <li className="list-item">
            <h3 className="thq-heading-3">Testimonials</h3>
            <p className="thq-body-small">
              Read what our satisfied clients have to say about our services and
              how we have helped them improve their online presence.
            </p>
          </li>
          <li className="list-item">
            <h3 className="thq-heading-3">Pricing Plans</h3>
            <p className="thq-body-small">
              Choose from our flexible pricing plans that cater to businesses of
              all sizes and budgets. Find the right plan for your specific
              needs.
            </p>
          </li>
        </ul>
      </div>
    </div>
  )
}

Stats8.defaultProps = {
  stat3ShortDescription: 'Website Performance Improvement',
  member12: 'Ankita Pancholi',
  member1Content3:
    'Ankita is a talented UI/UX designer with a passion for creating visually appealing and user-friendly interfaces.',
  stat4Description:
    'Clients who sign up for our services receive Google AdWords credits worth over $500 to boost their online presence.',
  member1Content1:
    'Ankita is a talented UI/UX designer with a passion for creating visually appealing and user-friendly interfaces.',
  member3Alt1: 'Michael Johnson - SEO Strategist',
  member3Content1:
    'Animesh specializes in optimizing websites to improve search engine visibility and drive organic traffic.',
  member1Alt1: 'John Doe - UI/UX Designer',
  member2Content2:
    "Vidya is a cybersecurity expert dedicated to ensuring the safety and protection of our clients' websites.",
  member2Job4: 'Security Specialist',
  member32: 'Animesh Awasthi',
  member1Content2:
    'Ankita is a talented UI/UX designer with a passion for creating visually appealing and user-friendly interfaces.',
  stat1: '95%',
  member3: 'Animesh Awasthi',
  member33: 'Animesh Awasthi',
  member14: 'Ankita Pancholi',
  member2Alt3: 'Jane Smith - Security Specialist',
  member2Content4:
    "Vidya is a cybersecurity expert dedicated to ensuring the safety and protection of our clients' websites.",
  member3Alt2: 'Michael Johnson - SEO Strategist',
  member2Job1: 'Security Specialist',
  member3Job1: 'SEO Strategist',
  member13: 'Ankita Pancholi',
  member21: 'Vidya Bharti',
  member3Content:
    'Animesh specializes in optimizing websites to improve search engine visibility and drive organic traffic.',
  member11: 'Ankita Pancholi',
  member1Job: 'UI/UX Designer',
  member3Job4: 'SEO Strategist',
  member1Content:
    'Ankita is a talented UI/UX designer with a passion for creating visually appealing and user-friendly interfaces.',
  member1Job3: 'UI/UX Designer',
  member1Job4: 'UI/UX Designer',
  member2Alt4: 'Jane Smith - Security Specialist',
  stat4ShortDescription: 'Google AdWords Credits',
  member2Alt1: 'Jane Smith - Security Specialist',
  member1: 'Ankita Pancholi',
  member23: 'Vidya Bharti',
  member1Alt: 'John Doe - UI/UX Designer',
  member1Job1: 'UI/UX Designer',
  member2Job2: 'Security Specialist',
  member1Alt3: 'John Doe - UI/UX Designer',
  stat3Description:
    'Our strategies have consistently led to a significant improvement in website performance for our clients.',
  member24: 'Vidya Bharti',
  stat1ShortDescription: 'Client Satisfaction Rate',
  member1Alt4: 'John Doe - UI/UX Designer',
  member3Content2:
    'Animesh specializes in optimizing websites to improve search engine visibility and drive organic traffic.',
  member3Content3:
    'Animesh specializes in optimizing websites to improve search engine visibility and drive organic traffic.',
  member3Alt: 'Michael Johnson - SEO Strategist',
  member3Job: 'SEO Strategist',
  member1Content4:
    'Ankita is a talented UI/UX designer with a passion for creating visually appealing and user-friendly interfaces.',
  member3Alt4: 'Michael Johnson - SEO Strategist',
  member3Job2: 'SEO Strategist',
  member3Alt3: 'Michael Johnson - SEO Strategist',
  heading1: 'Importance of this feauture.',
  member2Alt: 'Jane Smith - Security Specialist',
  member3Content4:
    'Animesh specializes in optimizing websites to improve search engine visibility and drive organic traffic.',
  member2Content1:
    "Vidya is a cybersecurity expert dedicated to ensuring the safety and protection of our clients' websites.",
  stat2ShortDescription: 'Projects Completed',
  member2: 'Vidya Bharti',
  member2Content:
    "Vidya is a cybersecurity expert dedicated to ensuring the safety and protection of our clients' websites.",
  member31: 'Animesh Awasthi',
  member34: 'Animesh Awasthi',
  stat4: '$500+',
  member2Job: 'Security Specialist',
  stat3: '98%',
  member1Job2: 'UI/UX Designer',
  member1Alt2: 'John Doe - UI/UX Designer',
  member2Job3: 'Security Specialist',
  member3Job3: 'SEO Strategist',
  member2Alt2: 'Jane Smith - Security Specialist',
  member22: 'Vidya Bharti',
  stat2: '200+',
  stat2Description:
    'With over 200 successful projects under our belt, we have the experience to take on any challenge.',
  member2Content3:
    "Vidya is a cybersecurity expert dedicated to ensuring the safety and protection of our clients' websites.",
}

Stats8.propTypes = {
  stat3ShortDescription: PropTypes.string,
  member12: PropTypes.string,
  member1Content3: PropTypes.string,
  stat4Description: PropTypes.string,
  member1Content1: PropTypes.string,
  member3Alt1: PropTypes.string,
  member3Content1: PropTypes.string,
  member1Alt1: PropTypes.string,
  member2Content2: PropTypes.string,
  member2Job4: PropTypes.string,
  member32: PropTypes.string,
  member1Content2: PropTypes.string,
  stat1: PropTypes.string,
  member3: PropTypes.string,
  member33: PropTypes.string,
  member14: PropTypes.string,
  member2Alt3: PropTypes.string,
  member2Content4: PropTypes.string,
  member3Alt2: PropTypes.string,
  member2Job1: PropTypes.string,
  member3Job1: PropTypes.string,
  member13: PropTypes.string,
  member21: PropTypes.string,
  member3Content: PropTypes.string,
  member11: PropTypes.string,
  member1Job: PropTypes.string,
  member3Job4: PropTypes.string,
  member1Content: PropTypes.string,
  member1Job3: PropTypes.string,
  member1Job4: PropTypes.string,
  member2Alt4: PropTypes.string,
  stat4ShortDescription: PropTypes.string,
  member2Alt1: PropTypes.string,
  member1: PropTypes.string,
  member23: PropTypes.string,
  member1Alt: PropTypes.string,
  member1Job1: PropTypes.string,
  member2Job2: PropTypes.string,
  member1Alt3: PropTypes.string,
  stat3Description: PropTypes.string,
  member24: PropTypes.string,
  stat1ShortDescription: PropTypes.string,
  member1Alt4: PropTypes.string,
  member3Content2: PropTypes.string,
  member3Content3: PropTypes.string,
  member3Alt: PropTypes.string,
  member3Job: PropTypes.string,
  member1Content4: PropTypes.string,
  member3Alt4: PropTypes.string,
  member3Job2: PropTypes.string,
  member3Alt3: PropTypes.string,
  heading1: PropTypes.string,
  member2Alt: PropTypes.string,
  member3Content4: PropTypes.string,
  member2Content1: PropTypes.string,
  stat2ShortDescription: PropTypes.string,
  member2: PropTypes.string,
  member2Content: PropTypes.string,
  member31: PropTypes.string,
  member34: PropTypes.string,
  stat4: PropTypes.string,
  member2Job: PropTypes.string,
  stat3: PropTypes.string,
  member1Job2: PropTypes.string,
  member1Alt2: PropTypes.string,
  member2Job3: PropTypes.string,
  member3Job3: PropTypes.string,
  member2Alt2: PropTypes.string,
  member22: PropTypes.string,
  stat2: PropTypes.string,
  stat2Description: PropTypes.string,
  member2Content3: PropTypes.string,
}

export default Stats8
