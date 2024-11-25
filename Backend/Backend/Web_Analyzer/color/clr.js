'use strict';

const postcss = require('postcss');
const Color = require('color');

function CssColorExtractor() {
  const propertiesWithColors = [
    'color',
    'background',
    'background-color',
    'background-image',
    'border',
    'border-top',
    'border-right',
    'border-bottom',
    'border-left',
    'border-color',
    'border-top-color',
    'border-right-color',
    'border-bottom-color',
    'border-left-color',
    'outline',
    'outline-color',
    'text-decoration',
    'text-decoration-color',
    'text-shadow',
    'box-shadow',
    'fill',
    'stroke',
    'stop-color',
    'flood-color',
    'lighting-color',
  ];
  const colorFormats = [
    'hexString',
    'hexaString',
    'rgbString',
    'percentString',
    'hslString',
    'hwbString',
    'keyword',
  ];

  function doesPropertyAllowColor(property) {
    return propertiesWithColors.indexOf(property) > -1;
  }

  function isColorGrey(color) {
    const red = color.red();

    return isColorMonochrome(color) && red > 0 && red < 255;
  }


  function isColorMonochrome(color) {
    const hsl = color.hsl().object();

    return hsl.h === 0 && hsl.s === 0;
  }


  function isValidColorFormat(format) {
    return colorFormats.indexOf(format) > -1;
  }


  function serializeColor(value, options) {
    if (!options.colorFormat || !isValidColorFormat(options.colorFormat)) {
      return value;
    }
    const color = new Color(value);
    let colorFormat = options.colorFormat;
    if (!color[options.colorFormat]) {
      colorFormat = colorFormat.replace(/String$/, '');
    }
    const formatted = color[colorFormat]();
    if (typeof formatted === 'string') {
      return formatted;
    }
    return formatted.string();
  }


  function defaultOptions(options) {
    return Object.assign({
      withoutGrey: false,
      withoutMonochrome: false,
      allColors: false,
      colorFormat: null,
      sort: null,
    }, options);
  }


  function sortColors(colors, sortOptions) {
    const options = defaultOptions(sortOptions);
    colors = colors.map((value) => serializeColor(value, options));
    if (options.sort === 'hue') {
      colors = colors.sort((a, b) => {
        return new Color(a).hue() - new Color(b).hue();
      });
    }
    if (options.sort === 'frequency') {
      const frequencyMap = new Map();
      colors.forEach((value) => {
        frequencyMap.set(value, (frequencyMap.get(value) || 0) + 1);
      });
      colors = colors.sort((a, b) => {
        return frequencyMap.get(b) - frequencyMap.get(a);
      });
    }
    return options.allColors ? colors : unique(colors);
  }


  function unique(items) {
    return [...new Set(items)];
  }

  function extractColorsFromString(string, options) {
    let colors = [];

    const {
      withoutMonochrome,
      withoutGrey,
      colorFormat,
    } = defaultOptions(options);

    postcss.list.comma(string).forEach(function(items) {
      postcss.list.space(items).forEach(function(item) {
        const regex = new RegExp(
          '^' +
                    '(-webkit-|-moz-|-o-)?' +
                    '(repeating-)?' +
                    '(radial|linear)-gradient\\((.*?)\\)' +
                    '$',
        );

        const match = item.match(regex);

        if (match) {
          colors = colors.concat.apply(
            colors,
            postcss.list.comma(match[4]).map(postcss.list.space),
          );
        } else {
          colors.push(item);
        }
      });
    });

    return colors.filter((value) => {
      let color;
      try {
        color = new Color(value);
      } catch (e) {
        return false;
      }

      if (withoutMonochrome && isColorMonochrome(color)) {
        return false;
      }

      if (withoutGrey && isColorGrey(color)) {
        return false;
      }

      if (colorFormat === 'keyword') {
        const keywordColor = new Color(color.keyword());
        if (keywordColor.rgbNumber() !== color.rgbNumber()) {
          return false;
        }
      }

      return true;
    });
  }

  function extractColorsFromDecl(decl, options) {
    if (!doesPropertyAllowColor(decl.prop)) {
      return [];
    }

    return extractColorsFromString(decl.value, options);
  }

  function extractColorsFromCss(css, options) {
    let colors = [];

    postcss.parse(css).walkDecls(function(decl) {
      colors = colors.concat(extractColorsFromDecl(decl, options));
    });

    return colors;
  }

  this.fromDecl = (decl, options) => sortColors(extractColorsFromDecl(decl, options), options);
  this.fromCss = (css, options) => sortColors(extractColorsFromCss(css, options), options);
  this.fromString = (string, options) => sortColors(extractColorsFromString(string, options), options);
}

module.exports = new CssColorExtractor();