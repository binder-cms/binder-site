<?php

namespace Tests\AppBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class IndexPageTest extends WebTestCase
{
    public function testIndex_getRootPath_hasExpectedSection()
    {
        $client = static::createClient();

        $crawler = $client->request('GET', '/');

        $this->assertNotEmpty($crawler->filter('section#what h2')->text());
    }

    public function testIndex_getIndexHtml_returnsOkStatus()
    {
        $client = static::createClient();

        $client->request('GET', '/index.html');

        $this->assertEquals(200, $client->getResponse()->getStatusCode());
    }

    public function testIndex_getIndexHtml_hasExpectedSection()
    {
        $client = static::createClient();

        $crawler = $client->request('GET', '/index.html');

        $this->assertNotEmpty($crawler->filter('section#what h2')->text());
    }
}
