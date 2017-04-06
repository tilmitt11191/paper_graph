<?php
/**
 * Stitch Theme Customizer
 *
 * @package Stitch
 * @since Stitch 1.0
 */

/**
 * Add postMessage support for site title and description for the Theme Customizer.
 *
 * @param WP_Customize_Manager $wp_customize Theme Customizer object.
 *
 * @since Stitch 1.2
 */
function stitch_customize_register( $wp_customize ) {

	$wp_customize->add_section( 'stitch_header', array(
		'title'          => __( 'Theme Options', 'stitch' ),
		'priority'       => 35,
	) );

	$wp_customize->add_setting( 'header_position', array(
	    'default'        => 'true',
	    'type'           => 'theme_mod',
	    'capability'     => 'edit_theme_options',
	) );

	$wp_customize->add_control( 'fix_header_position', array(
	    'settings' => 'header_position',
	    'label'    => __( 'Fixed Header Position (works best with a short menu and sidebar)', 'stitch' ),
	    'section'  => 'stitch_header',
	    'type'     => 'checkbox',
	) );

}
add_action( 'customize_register', 'stitch_customize_register' );