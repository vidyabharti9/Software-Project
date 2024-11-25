import React from "react";

import PropTypes from "prop-types";

import "./features21.css";

const Features21 = (props) => {
  return (
    <div className="features21-layout302 thq-section-padding">
      <div className="features21-max-width thq-section-max-width">
        <div className="features21-section-title thq-flex-column">
          <h2 className="thq-heading-2">{props.sectionTitle}</h2>
          <p className="thq-body-large">{props.sectionDescription}</p>
        </div>
        <div className="features21-content1">
          <div className="thq-grid-5">
            <div className="features21-feature1 thq-flex-column">
              <img
                alt={props.feature1ImageAlt}
                src="https://play.teleporthq.io/static/svg/default-img.svg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature1Title}</h3>
                <span className="thq-body-small">
                  {props.feature1Description}
                </span>
              </div>
            </div>
            <div className="features21-feature2 thq-flex-column">
              <img
                alt={props.feature2ImageAlt}
                src="https://play.teleporthq.io/static/svg/default-img.svg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature2Title}</h3>
                <span className="thq-body-small">
                  {props.feature2Description}
                </span>
              </div>
            </div>
            <div className="features21-feature3 thq-flex-column">
              <img
                alt={props.feature3ImageAlt}
                src="https://play.teleporthq.io/static/svg/default-img.svg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature3Title}</h3>
                <span className="thq-body-small">
                  {props.feature3Description}
                </span>
              </div>
            </div>
            <div className="features21-feature4 thq-flex-column">
              <img
                alt={props.feature4ImageAlt}
                src="https://play.teleporthq.io/static/svg/default-img.svg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature4Title}</h3>
                <span className="thq-body-small">
                  {props.feature4Description}
                </span>
              </div>
            </div>
            <div className="features21-feature5 thq-flex-column">
              <img
                alt={props.feature5ImageAlt}
                src="https://play.teleporthq.io/static/svg/default-img.svg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature5Title}</h3>
                <span className="thq-body-small">
                  {props.feature5Description}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

Features21.defaultProps = {
  feature1Description:
    "Enhance user experience with visually appealing and intuitive design elements.",
  feature4Title: "Expert Assistance",
  feature4Description:
    "Get guidance and support from our team of experienced professionals.",
  feature1ImageAlt: "UI/UX Design Image",
  feature5Description:
    "Receive credits to kickstart your online advertising campaigns and reach a wider audience.",
  sectionDescription:
    "Explore the features that set us apart and help elevate your website performance.",
  mainAction: "Choose Your Plan",
  feature2Description:
    "Protect your website and user data with robust security measures.",
  feature3Description:
    "Improve search engine visibility and drive organic traffic to your website.",
  feature4ImageAlt: "Expert Assistance Image",
  feature2ImageAlt: "Security Solutions Image",
  feature5ImageAlt: "Google AdWords Credits Image",
  sectionTitle: "Key Features",
  feature5Title: "Google AdWords Credits",
  feature2ImageSrc:
    "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5MTMyMXwwfDF8cmFuZG9tfHx8fHx8fHx8MTcyMTMyMDIwN3w&ixlib=rb-4.0.3&q=80&w=1080",
  feature3Title: "SEO Strategies",
  feature3ImageAlt: "SEO Strategies Image",
  feature4ImageSrc:
    "https://images.unsplash.com/photo-1470790376778-a9fbc86d70e2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5MTMyMXwwfDF8cmFuZG9tfHx8fHx8fHx8MTcyMTMyMDIwNnw&ixlib=rb-4.0.3&q=80&w=1080",
  feature2Title: "Security Solutions",
  feature1Title: "UI/UX Design",
};

Features21.propTypes = {
  feature1Description: PropTypes.string,
  feature4Title: PropTypes.string,
  feature4Description: PropTypes.string,
  feature1ImageAlt: PropTypes.string,
  feature5Description: PropTypes.string,
  sectionDescription: PropTypes.string,
  mainAction: PropTypes.string,
  feature2Description: PropTypes.string,
  feature3Description: PropTypes.string,
  feature4ImageAlt: PropTypes.string,
  feature2ImageAlt: PropTypes.string,
  feature5ImageAlt: PropTypes.string,
  sectionTitle: PropTypes.string,
  feature5Title: PropTypes.string,
  feature2ImageSrc: PropTypes.string,
  feature3Title: PropTypes.string,
  feature3ImageAlt: PropTypes.string,
  feature4ImageSrc: PropTypes.string,
  feature2Title: PropTypes.string,
  feature1Title: PropTypes.string,
};

export default Features21;