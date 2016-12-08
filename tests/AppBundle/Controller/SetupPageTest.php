<?php

namespace AppBundle\Controller;


use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class SetupPageTest extends WebTestCase
{
    public function testSetup_getHtml_returnsOk()
    {
        $client = static::createClient();

        $client->request('GET', '/setup.html');

        $this->assertEquals(200, $client->getResponse()->getStatusCode());
    }

    public function testIndex_getHtml_hasExpectedTitle()
    {
        $client = static::createClient();

        $crawler = $client->request('GET', '/setup.html');

        $this->assertContains('Setup', $crawler->filter('h1')->text());
    }

    public function testSetup_getAsDirectory_returnsNotFound()
    {
        $client = static::createClient();

        // The template for this URL would be located at
        // app/Resources/views/pages/setup/index.html.twig
        $client->request('GET', '/setup/');

        $this->assertEquals(404, $client->getResponse()->getStatusCode());
    }
}
