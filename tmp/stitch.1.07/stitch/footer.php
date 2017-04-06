<?php
/**
 * The template for displaying the footer.
 *
 * Contains the closing of the id=main div and all content after
 *
 * @package Stitch
 * @since Stitch 1.0
 */
?>

	</div><!-- #main .site-main -->

	<footer id="colophon" class="site-footer" role="contentinfo">
		<div class="site-info">
			<?php do_action( 'stitch_credits' ); ?>
			<a href="http://wordpress.org/" title="<?php esc_attr_e( 'A Semantic Personal Publishing Platform', 'stitch' ); ?>" rel="generator"><?php printf( __( 'Proudly powered by %s', 'stitch' ), 'WordPress' ); ?></a>
			<span class="sep">  </span>
			<?php printf( __( 'Theme: %1$s by %2$s.', 'stitch' ), 'Stitch', '<a href="http://carolinemoore.net/" rel="designer">Caroline Moore</a>' ); ?>
		</div><!-- .site-info -->
	</footer><!-- #colophon .site-footer -->
</div><!-- #page .hfeed .site -->

<?php wp_footer(); ?>

</body>
</html>