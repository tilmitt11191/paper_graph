<?php
/**
 * Sample implementation of the Custom Header feature
 * http://codex.wordpress.org/Custom_Headers
 *
 * You can add an optional custom header image to header.php like so ...

	<?php $header_image = get_header_image();
	if ( ! empty( $header_image ) ) { ?>
		<a href="<?php echo esc_url( home_url( '/' ) ); ?>" title="<?php echo esc_attr( get_bloginfo( 'name', 'display' ) ); ?>" rel="home">
			<img src="<?php header_image(); ?>" width="<?php echo get_custom_header()->width; ?>" height="<?php echo get_custom_header()->height; ?>" alt="" />
		</a>
	<?php } // if ( ! empty( $header_image ) ) ?>

 *
 * @package Stitch
 * @since Stitch 1.0
 */

/**
 * Setup the WordPress core custom header feature.
 *
 * Use add_theme_support to register support for WordPress 3.4+
 * as well as provide backward compatibility for previous versions.
 * Use feature detection of wp_get_theme() which was introduced
 * in WordPress 3.4.
 *
 * @todo Rework this function to remove WordPress 3.4 support when WordPress 3.6 is released.
 *
 * @uses stitch_header_style()
 * @uses stitch_admin_header_style()
 * @uses stitch_admin_header_image()
 *
 * @package Stitch
 */
function stitch_custom_header_setup() {
	$args = array(
		'default-image'          => '',
		'default-text-color'     => 'fff',
		'width'                  => 350,
		'height'                 => 350,
		'flex-height'            => true,
		'wp-head-callback'       => 'stitch_header_style',
		'admin-head-callback'    => 'stitch_admin_header_style',
		'admin-preview-callback' => 'stitch_admin_header_image',
	);

	$args = apply_filters( 'stitch_custom_header_args', $args );

	if ( function_exists( 'wp_get_theme' ) ) {
		add_theme_support( 'custom-header', $args );
	} else {
		// Compat: Versions of WordPress prior to 3.4.
		define( 'HEADER_TEXTCOLOR',    $args['default-text-color'] );
		define( 'HEADER_IMAGE',        $args['default-image'] );
		define( 'HEADER_IMAGE_WIDTH',  $args['width'] );
		define( 'HEADER_IMAGE_HEIGHT', $args['height'] );
		add_custom_image_header( $args['wp-head-callback'], $args['admin-head-callback'], $args['admin-preview-callback'] );
	}
}
add_action( 'after_setup_theme', 'stitch_custom_header_setup' );

/**
 * Shiv for get_custom_header().
 *
 * get_custom_header() was introduced to WordPress
 * in version 3.4. To provide backward compatibility
 * with previous versions, we will define our own version
 * of this function.
 *
 * @todo Remove this function when WordPress 3.6 is released.
 * @return stdClass All properties represent attributes of the curent header image.
 *
 * @package Stitch
 * @since Stitch 1.1
 */

if ( ! function_exists( 'get_custom_header' ) ) {
	function get_custom_header() {
		return (object) array(
			'url'           => get_header_image(),
			'thumbnail_url' => get_header_image(),
			'width'         => HEADER_IMAGE_WIDTH,
			'height'        => HEADER_IMAGE_HEIGHT,
		);
	}
}

if ( ! function_exists( 'stitch_header_style' ) ) :
/**
 * Styles the header image and text displayed on the blog
 *
 * @see stitch_custom_header_setup().
 *
 * @since Stitch 1.0
 */
function stitch_header_style() {

	// If no custom options for text are set, let's bail
	// get_header_textcolor() options: HEADER_TEXTCOLOR is default, hide text (returns 'blank') or any hex value
	if ( HEADER_TEXTCOLOR == get_header_textcolor() )
		return;
	// If we get this far, we have custom styles. Let's do this.
	?>
	<style type="text/css">
	<?php
		// Has the text been hidden?
		if ( 'blank' == get_header_textcolor() ) :
	?>
		.site-title,
		.site-description {
			position: absolute !important;
			clip: rect(1px 1px 1px 1px); /* IE6, IE7 */
			clip: rect(1px, 1px, 1px, 1px);
		}
	<?php
		// If the user has set a custom color for the text use that
		else :
	?>
		.site-title a,
		.site-description {
			color: #<?php echo get_header_textcolor(); ?> !important;
		}
	<?php endif; ?>
	</style>
	<?php
}
endif; // stitch_header_style

if ( ! function_exists( 'stitch_admin_header_style' ) ) :
/**
 * Styles the header image displayed on the Appearance > Header admin panel.
 *
 * @see stitch_custom_header_setup().
 *
 * @since Stitch 1.0
 */
function stitch_admin_header_style() {
?>
	<style type="text/css">
	.appearance_page_custom-header #headimg {
		background: url( '<?php echo get_template_directory_uri(); ?>/images/background.jpg' );
		background-size: 400px auto;
		border: none;
		max-width: 363px;
	}
	#headimg h1,
	#desc {
	}
	#headimg h1 {
		margin-bottom: 18px;
		margin-left: 0;
		margin-right: 0;
		margin-top: 32.4px;
	}
	#headimg h1 a {
		background: #b7e8d4;
		border-radius: 50%;
		box-shadow: 0 0 5px 2px rgba(0,0,0,1);
		color: #fff;
		display: table;
		font-family: "Fjalla One", Helvetica, Arial, sans-serif;
		font-size: 30px;
		line-height: 1;
		margin: 0 auto;
		overflow: hidden;
		padding: 12px;
		position: relative;
		text-align: center;
		text-decoration: none;
		text-shadow: 1px 1px 3px rgba(0,0,0,.2);
		text-transform: uppercase;
		width: 170px;
		height: 170px;
	}
	#headimg h1 a span {
		border: 1px dashed #fff;
		border-radius: 50%;
		display: table-cell;
		overflow: hidden;
		vertical-align: middle;
		max-width: 170px;
		max-height: 170px;
	}
	#desc {
		color: #fff;
		display: block;
		font-family: "Pacifico", script;
		font-size: 20px;
		font-variant: normal;
		line-height: 1.6;
		margin: 0 auto;
		text-align: center;
		width: 80%;
	}
	#headimg img {
		display: block;
		margin: 0 auto;
	}
	</style>
<?php
}
endif; // stitch_admin_header_style

if ( ! function_exists( 'stitch_admin_header_image' ) ) :
/**
 * Custom header image markup displayed on the Appearance > Header admin panel.
 *
 * @see stitch_custom_header_setup().
 *
 * @since Stitch 1.0
 */
function stitch_admin_header_image() { ?>
	<div id="headimg">
		<?php
		if ( 'blank' == get_header_textcolor() || '' == get_header_textcolor() )
			$style = ' style="display:none;"';
		else
			$style = ' style="color:#' . get_header_textcolor() . ';"';
		?>
		<?php $header_image = get_header_image();
		if ( ! empty( $header_image ) ) : ?>
			<img src="<?php echo esc_url( $header_image ); ?>" alt="" />
		<?php endif; ?>
		<h1><a id="name"<?php echo $style; ?> onclick="return false;" href="<?php echo esc_url( home_url( '/' ) ); ?>"><span class="site-title-wrapper"><?php bloginfo( 'name' ); ?></span></a></h1>
		<div id="desc"<?php echo $style; ?>><?php bloginfo( 'description' ); ?></div>
	</div>
<?php }
endif; // stitch_admin_header_image