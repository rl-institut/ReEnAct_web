
/* globals capacitiesChanged */

const colors = JSON.parse(document.getElementById("slider_colors").textContent);
const dependencies = JSON.parse(document.getElementById("slider_dependencies").textContent);


$(".js-range-slider").ionRangeSlider({
  onFinish: function (data) {
    handleSliderDependencies(data);
    updateColors();
    capacitiesChanged();  // in myplan.js
  }
});


function handleSliderDependencies(data) {
  const id   = data.input.attr('id');    // e.g. "id_marsh", "id_paludiculture", "id_pv_marsh"
  const name = id.slice(3);              // remove "id_"
  const val  = data.from;                // current slider value

  // --- 1) STATIC MAX Dependencies (unchanged) ---
  if (name === "marsh") {
    Object.entries(dependencies.areas_at_full_marsh_usage).forEach(([target, area]) => {
      const ratio = area / dependencies.marsh_max_area;
      const newMax = Math.round(val * ratio * dependencies.densities[target]);
      $('#id_' + target)
        .data('ionRangeSlider')
        .update({ max: newMax });
    });
  }

  // --- 2) COMPETITION: adjust only 'from', not max ---
  // sum of areas (ha) for biomass & pv_marsh ≤ marsh * sum_ratio
  const marshHa = $('#id_marsh').data('ionRangeSlider').result.from;

  if (name === 'biomass_marsh') {
    // user moved biomass → compute allowed pv_marsh area
    const biomassTM   = val;
    const biomassHa   = biomassTM / dependencies.densities.biomass_marsh;
    let allowedPvHa = marshHa - biomassHa;
    if (allowedPvHa < 0) allowedPvHa = 0;
    const allowedPvMW = allowedPvHa * dependencies.densities.pv_marsh;

    const pvSlider   = $('#id_pv_marsh').data('ionRangeSlider');
    const currentPv  = pvSlider.result.from;  // in ha

    // only update if current Pv > allowedPv
    if (currentPv > allowedPvMW) {
      pvSlider.update({ from: allowedPvMW });
    }
  }
  if (name === 'pv_marsh') {
    // user moved pv_marsh → compute allowed biomass TM
    const pvMW = val;
    const pvHa = pvMW / dependencies.densities.pv_marsh;
    let allowedBiomassHa = marshHa - pvHa;
    if (allowedBiomassHa < 0) allowedBiomassHa = 0;
    const allowedBiomassTM = Math.round(allowedBiomassHa * dependencies.densities.biomass_marsh);

    const biomassSlider  = $('#id_biomass_marsh').data('ionRangeSlider');
    const currentBiomass = biomassSlider.result.from; // in TM

    // only update if current Palu TM > allowed Palu TM
    if (currentBiomass > allowedBiomassTM) {
      biomassSlider.update({ from: allowedBiomassTM });
    }
  }
}

// updateSliderMarks();
updateColors();

// Update the colors of the sliders based on the color scheme and the contrast ratio with white text
function getLuminance(rgb) {
  const [r, g, b] = rgb.map(c => {
    c /= 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrastRatio(rgb1, rgb2) {
  const lum1 = getLuminance(rgb1);
  const lum2 = getLuminance(rgb2);
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

function hexToRgb(hex) {
  const bigint = parseInt(hex.slice(1), 16);
  return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
}

function updateColors() {
  document.getElementById("capacityForm").querySelectorAll("input").forEach(function(item) {
    const sliderColor = colors[item.id.slice(3)];
    if (sliderColor !== undefined) {
      const rgb = hexToRgb(sliderColor);
      const white = [255, 255, 255];
      const textColor = contrastRatio(rgb, white) >= 4.5 ? "#ffffff" : "#000000";

      item.parentElement.querySelector(".irs-bar").style.backgroundColor = sliderColor;
      const irsSingle = item.parentElement.querySelector(".irs-single");
      irsSingle.style.backgroundColor = sliderColor;
      irsSingle.style.color = textColor;
    }
  });
}

function convertToPercent(num, min, max) {
  return ((num - min) / (max - min)) * 100;
}

function addMark(data, category, markValue) {
  let percent = convertToPercent(markValue, data.min, data.max);
  // Fix percentage due to offset
  percent = percent - (3.5 * percent) / 100;
  const html = `<span class="showcase__mark_${category}" style="left: ${percent}%"></span>`;
  data.slider.append(html);
}

function updateSliderMarks() {
  const sliderMarks = JSON.parse(document.getElementById('slider_marks').textContent);
  for (const category in sliderMarks) {
    for (const mark of sliderMarks[category]) {
      const sliderName = mark[0];
      const sliderValues = mark[1];
      let slider = $(`#id_${sliderName}`).data("ionRangeSlider");
      slider.update({
        // jshint ignore:start
        onUpdate: function (data) {
          let i = 0;
          for (const sliderValue of sliderValues) {
            if (i > 0) {
              // Add a different marker (greyed out) after the first marker
              addMark(data, "distance", sliderValue);
            } else {
              addMark(data, category, sliderValue);
            }
            i += 1;
          }
        },
        // jshint ignore:end
      });
    }
  }
}

$(document).ready(function() {
  const marshSlider = $("#id_marsh").data("ionRangeSlider");
  handleSliderDependencies({
    input: $("#id_marsh"),
    from:  marshSlider.result.from
  });
  updateSliderMarks();
  updateColors();
});
