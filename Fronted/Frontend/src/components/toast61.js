import React from 'react'

import PropTypes from 'prop-types'

import './toast61.css'

const Toast61 = (props) => {
  return (
    <div className={`toast61-container ${props.rootClassName} `}>
      <div className="toast61-header">
        <h2 className="thq-heading-2">{props.bannerTitle}</h2>
      </div>
    </div>
  )
}

Toast61.defaultProps = {
  bannerTitle: 'Search Engine Optimization Features',
  rootClassName: '',
}

Toast61.propTypes = {
  bannerTitle: PropTypes.string,
  rootClassName: PropTypes.string,
}

export default Toast61
